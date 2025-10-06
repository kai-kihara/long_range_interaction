from dataclasses import dataclass

@dataclass
class SystemParams:
    L:int #サイト数
    t_max:int #総ステップ数
    dt:float #時間幅(小さいほど大きい確率に対応できるが、その分十分なサンプルをとるのに大きいステップ数を必要とする)

if __name__ == '__main__':
    pass