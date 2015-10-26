# soracom-remote

SORACOM Air端末の簡易コンソール

## Description

いつでも自由に設定変更可能なSORACOMのSIMを、データ通信端末やスマホで必要なときに帯域をあげたりさげたりするため、簡単なUI（スマホ画面対応）でコントロールできるようにしました。

簡易的な実装に留めているので、実際に利用する際はご注意を。

***Screen:***

![SORACOM-Remote](https://s3-ap-northeast-1.amazonaws.com/soracom-remote/SORACOM-Remote.png)

## Features

- SIMの一覧表示（Nameタグ、IMSI番号、ステータス、速度タイプ）
- 利用開始、休止（activate/deactivate)
- 速度タイプ変更


## Requirement

- Python 2.5 or higher
- Flask [Flask (A Python Microframework)](http://flask.pocoo.org/)
- httplib2 [jcgregorio/httplib2 · GitHub](https://github.com/jcgregorio/httplib2)

## Usage

1. アプリケーション起動
```
	$ sudo app.py
```
2. ブラウザで `http://x.x.x.x/` へアクセス

## Installation

	$ pip install Flask
	$ pip install httplib2
	$ git clone https://github.com/kazgoto/soracom-remote.git

## Author

[@kaz_goto](https://twitter.com/kaz_goto)

## License

[MIT](https://raw.githubusercontent.com/b4b4r07/dotfiles/master/doc/LICENSE-MIT.txt)
