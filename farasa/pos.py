from .__base import FarasaBase


class TaggedToken:
    def __init__(self, token, tag):
        self.tokens, self.tags = list(), list()
        self.tokens.append(token)
        self.tags.append(tag)

    def append_connected_token(self, token=None, tag=None, tagged_token=None):
        assert not (token and tag) or not tagged_token
        if tagged_token:
            self.tokens.extend(tagged_token.tokens)
            self.tags.extend(tagged_token.tags)

        else:
            self.tokens.append(token)
            self.tags.append(tag)

    @property
    def last_token(self):
        return self.tokens[-1]

    # def raise_value_error(self):
    #     raise ValueError("Tagged Token object cannot have more than three subtokens")

    def _process_tag(self, tag):
        subtags = tag.split("-")
        if len(subtags) == 1:
            return subtags
        else:
            return (subtags[0], *list(subtags[1]))

    def process_tags(self):
        processed_tags = list()
        for tag in self.tags:
            processed_subtags = list()
            subtags = tag.split("-")
            processed_subtags.append(subtags[0])
            if len(subtags) > 1:
                for subtag in subtags[1:]:
                    processed_subtags.append(tuple(subtag))
            processed_tags.append(processed_subtags)
        return tuple(processed_tags)

    def as_tuple(self):
        return (
            "".join(token.strip() for token in self.tokens).replace("+", ""),
            # *list(self._process_tag(tag) for tag in self.tags),
            self.process_tags(),
        )

    def __str__(self):
        return str(self.as_tuple())

    def __repr__(self):
        return str(self.as_tuple())


class FarasaPOSTagger(FarasaBase):
    task = "POS"

    def tag(self, text):
        return self._do_task(text=text)

    def tag_segments(self, text, combine_subtokens=False):
        tokens_objects = list()
        tagged_text = self.tag(text)
        # ignore the first and last as they are indications of
        #  the begining and end of the string
        tagged_tokens = tagged_text.split()[1:-1]
        if not combine_subtokens:
            for tagged_token in tagged_tokens:
                token, tag = tagged_token.split("/")
                token_object = TaggedToken(token, tag)
                if not tokens_objects:
                    tokens_objects.append(token_object)
                elif tokens_objects[-1].last_token[-1] == "+":
                    tokens_objects[-1].append_connected_token(tagged_token=token_object)
                elif token_object.last_token[0] == "+":
                    tokens_objects[-1].append_connected_token(tagged_token=token_object)
                else:
                    tokens_objects.append(token_object)
            return tokens_objects
        else:
            tokens_objects = [
                TaggedToken(*tagged_token.split("/")) for tagged_token in tagged_tokens
            ]
            return tokens_objects

