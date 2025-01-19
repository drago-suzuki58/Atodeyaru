# Atodeyaru

Atodeyaru(あとでやる)は、全く新しいタスクスケジューリングライブラリです。

Other Language README  
[English](README.en.md)

## 特徴

- 期限：  
  夏休みの宿題のように、期限を設けてそれまでに実行。
- 気まぐれな実行：  
  もしかしたらやる気が出て期限よりも早く実行するかもしれないし、期限ギリギリまで後回しにするかもしれません。
- 現実逃避：  
  「あのタスク嫌だな」「こっち先にやるか」みたいなテスト期間に掃除が捗る現象を再現しました。
- バックグラウンド実行：  
  バックグラウンドで行われるので、メインの処理を邪魔しません。

## インストール方法

GitHubリポジトリからインストールできます。

```sh
python -m pip install git+https://github.com/drago-suzuki58/Atodeyaru
```

## 使い方

### `Atodeyaru` インスタンスの作成

`Atodeyaru` を使うには、まずインスタンスを作成します。

```python
from atodeyaru import Atode

# 基本的なAtodeyaruインスタンスを作成
atode = Atode()

# デーモンスレッドとして実行するAtodeyaruインスタンスを作成
# daemon=True にすると、メインの処理が終了してもバックグラウンドでタスクを実行し続けます。
atode_daemon = Atode(daemon=True)
```

`daemon=True` を指定すると、`Atodeyaru` が管理するスレッドはデーモンスレッドとして動作します。これは、メインのプログラムが終了しても、バックグラウンドでタスクの実行を継続したい場合に便利です。デフォルトは `False` です。  
詳細は`threading`ライブラリを調べてください。

### タスクの登録 (`yaru` メソッド)

`yaru` メソッドを使って、実行したい関数を `Atodeyaru` に登録します。

```python
import time
from atodeyaru import Atode

atode = Atode()

def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")
    time.sleep(1)

# 5秒後までくらいに 'Alice' に挨拶するタスクを登録
atode.yaru(greet, deadline_sec=5, args=("Alice",))

# 'Bob' に「Good morning」と挨拶するタスクを登録 (締め切りなし)
atode.yaru(greet, args=("Bob",), kwargs={"greeting": "Good morning"})

# 別の関数も登録可能
def another_task():
    print("Another task is running...")

atode.yaru(another_task)

time.sleep(10)
atode.stop()
```

- **`func`**:  
  実行したい関数オブジェクトを指定します。
- **`deadline_sec` (オプション)**:  
  タスクを実行したいおおよその秒数を指定します。`None` を指定すると、締め切りのないタスクとして登録されます。
- **`args` (オプション)**:  
  関数に渡す位置引数のタプルを指定します。上記の例では、`greet` 関数に `"Alice"` という引数を渡しています。
- **`kwargs` (オプション)**:  
  関数に渡すキーワード引数の辞書を指定します。上記の例では、`greet` 関数に `greeting="Good morning"` というキーワード引数を渡しています。

### `Atodeyaru` を止めるには

```python
atode = Atode()
# ... タスクの登録 ...

# Atodeyaruのバックグラウンドスレッドを停止
atode.stop()

# 強制的に停止する場合は force=True を指定(実行中のタスクが中断される可能性あり)
atode.stop(force=True)
```

`stop()` メソッドは、`Atodeyaru` が管理するバックグラウンドスレッドを停止します。

- `force=False` (デフォルト):  
  `Atodeyaru` は、まだ実行されていないタスクがなくなるまで待ち、その後スレッドを停止します。
- `force=True`:  
  実行中のタスクを中断し、直ちにスレッドを停止します。データの不整合などが起こる可能性があるため、注意して使用してください。

## 注意

このライブラリはお分かりの通り厳密な使い方には向きません。  
あくまでネタとして使ってください。
