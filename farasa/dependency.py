from .__base import FarasaBase


class FarasaDepParser(FarasaBase):
    task = "depparse"

    def parse(self, text):
        return self._do_task(text=text)
    
    def parse_segments(self, text):
        parse_result = self._do_task(text=text).split('\n')
        docs = []
        result = []
        for row in parse_result:
            if row == '':
                # docs.append(result)
                # result = []
                continue
            i, word, lemma, pos, xpos, *morph, head_i, dep = row.split('\t')
            i = int(i) - 1
            head_i = int(head_i)
            if dep == "---":
                dep = "root"
            else:
                head_i -= 1

            morph = f"dict({', '.join(morph)})"
            # morph = eval(morph)
            result.append({
                "i": i,
                # "head": head,
                "dep": dep.lower(),
                "pos": pos.upper(),
                "lemma": lemma,
                "morph": morph,
                "text": word,
                "head_i": head_i,
            })

        for i in range(len(result)):
            h_i =  result[i]['head_i']
            result[i]['head'] = result[h_i]['text']

        docs.append(result)
        return result

