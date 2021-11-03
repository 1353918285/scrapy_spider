def transform(s):
    if s.endswith('月'):
        data = s.split('/')[0]
        if data.endswith('万'):
            sal = data.split('-')
            min = int(float(sal[0]) * 10000)
            max = int(float(sal[1].replace('万', '')) * 10000)
            avg = (min + max) / 2
            return avg
        if data.endswith('千'):
            sal = data.split('-')
            min = int(float(sal[0]) * 1000)
            max = float(sal[1].replace('千', '')) * 1000
            avg = (min + max) / 2
            return avg
    if s.endswith('年'):
        data = s.split('/')[0]
        if data.endswith("万"):
            sal = data.split("-")
            min = float(sal[0]) * 10000 / 12
            max = float(sal[1].replace('万', '')) * 10000 / 12
            avg = int((min + max) / 2)
            return avg
    if s.endswith('天'):
        data = s.split('/')[0]
        avg = float(data.replace('元', '')) * 30
        return avg
    if s.endswith('时'):
        data = s.split("/")[0]
        avg = float(data.replace('元',''))*8*30
        return avg

    else:
        return s
