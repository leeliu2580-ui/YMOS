from tickflow import TickFlow


def main():
    try:
        # 使用免费服务（无需 API key）
        tf = TickFlow.free()

        # 查询日K线数据
        df = tf.klines.get("600000.SH", period="1d", count=100, as_dataframe=True)
        print("=== 600000.SH 日K线最近几条 ===")
        print(df.tail())

        # 查询标的信息
        instruments = tf.instruments.batch(symbols=["600000.SH", "000001.SZ"])
        print("\n=== 标的信息 ===")
        print(instruments)

    except ModuleNotFoundError:
        print("未安装 tickflow，请先运行：")
        print("python -m pip install tickflow")
    except Exception as e:
        print(f"运行出错: {e}")


if __name__ == "__main__":
    main()
