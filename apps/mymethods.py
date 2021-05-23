def lastone(iterable):
    """与えられたイテレータブルオブジェクトの
    最後の一つの要素の時にTrue、それ以外の時にFalseを返す.
    """
    # イテレータを取得して最初の値を取得する
    if iterable:
        it = iter(iterable)
        try:
            last = next(it)
            # 2番目の値から開始して反復子を使い果たすまで実行
            for val in it:
                # 一つ前の値を返す
                yield last, False
                last = val  # 値の更新
            # 最後の一つ
            yield last, True
        except StopIteration:
            yield None, True

    else:
        yield None, True


def dainyu(x, y=None):
    if x is None:
        ans = y
    else:
        ans = x
    return ans
