import pytest

df = pd.read_json('prediction24.json')


def test_len(df):
    print(len(df))
    assert len(df) == 24

if __name__ == '__main__':
    pytest.main()

    