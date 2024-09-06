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

    @property
    def command(self):
        return self.BASE_CMD + [str(self.bin_dir / "FarasaPOSJar.jar")]

    task = "POS"

    def tag(self, text):
        return self._do_task(text=text)

    def tag_segments(self, text, combine_subtokens=False):
        tokens_objects = list()
        tagged_text = self.tag(text)
        # ignore the first and last as they are indications of
        #  the begining and end of the string
        tagged_tokens = tagged_text.split()[1:-1]
        subtokens = list()
        for tagged_token in tagged_tokens:
            slash_count = self._count_slashes(tagged_token)
            # if there is no slash, then this must have been a subtoken
            if slash_count == 0:
                subtokens.append(tagged_token)
            # check if the token has multiple slashes ex: date 19/5/1955 or a single slash
            elif slash_count > 1:
                token = "/".join(tagged_token.split("/")[0:-1])
                tag = tagged_token.split("/")[-1]
                tokens_objects.append(TaggedToken(token, tag))
            else:
                temp_token, temp_tag = tagged_token.split("/")
                if len(subtokens) > 0:
                    subtokens.append(temp_token)
                    temp_tags = temp_tag.split("+")
                    assert len(subtokens) == len(temp_tags)
                    if combine_subtokens:
                        tokens_object = TaggedToken(subtokens[0], temp_tags[0])
                        for _token, _tag in zip(subtokens[1:], temp_tags[1:]):
                            tokens_object.append_connected_token(token=_token, tag=_tag)
                        tokens_objects.append(tokens_object)
                    else:
                        for _token, _tag in zip(subtokens, temp_tags):
                            tokens_objects.append(TaggedToken(_token, _tag))
                    subtokens = list()
                else:
                    tokens_objects.append(TaggedToken(temp_token, temp_tag))
        return tokens_objects

    def _count_slashes(self, text: str):
        # this is the faster counter implementation for very short text
        slash_counter = 0
        for c in text:
            if c == "/":
                slash_counter += 1
        return slash_counter
