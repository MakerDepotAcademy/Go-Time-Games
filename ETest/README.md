# Quiz Show

This is the display component of the quiz show

- [Quiz Show](#quiz-show)
  - [Installation](#installation)
  - [Usage](#usage)
    - [GET /](#get)
    - [DELETE /](#delete)
    - [POST /question](#post-question)
      - [Example:](#example)
    - [POST /answer/:label](#post-answerlabel)
      - [Example:](#example-1)
    - [POST /answer/:label/correct](#post-answerlabelcorrect)
    - [POST /start](#post-start)
      - [Example:](#example-2)
    - [GET /score](#get-score)
      - [Example:](#example-3)
    - [POST /score](#post-score)
      - [Example:](#example-4)
    - [POST /score/inc](#post-scoreinc)
      - [Example:](#example-5)
    - [POST /score/dec](#post-scoredec)
      - [Example:](#example-6)
    - [POST /subscribe/:event](#post-subscribeevent)
      - [Events:](#events)
      - [Example:](#example-7)

## Installation

``` bash
cd ETest
npm install
```

## Usage

All interactions are done via `http` on port `8080`

### GET /

Does a health check

### DELETE /

Quits the display

### POST /question

Sets the question to display

#### Example:

```bash 
curl -i http://localhost:8080/question -X POST -d 'What is my name'
```

### POST /answer/:label

Set the answer to a question. `:label` must be in `/[a-d]/`

#### Example:

```bash
curl -i http://localhost:8080/answer/a -X POST -d 'Dan'
```

### POST /answer/:label/correct

Changes the answer of content in `:label` to correct. Halts the round

### POST /start

Starts the round. If this is the first call, will also start game timer

#### Example:

```bash
curl -i http://localhost:8080/start -X POST
```

### GET /score

Returns the current score

#### Example:

```bash
curl -i http://localhost:8080/score
```

### POST /score

Sets the score

#### Example:

```bash
curl -i http://localhost:8080/score -X POST -d '100'
```

### POST /score/inc

Adds to the score

#### Example:

```bash
curl -i http://localhost:8080/score/inc -X POST -d '10'
```

### POST /score/dec

Subtracts to the score

#### Example:

```bash
curl -i http://localhost:8080/score/dec -X POST -d '10'
```

### POST /subscribe/:event

Adds an event hook to the game. Each time an event is triggered, every url subscribed will receive an empty `GET` request.

#### Events:

* `roundover`: emitted when the round timer reaches 0
* `gameover`: emitted when game is over
* `scorechanged`: emitted when score is changed

#### Example:

```bash
curl -i http://localhost:8080/subscribe/gameover -X POST -d 'http://192.168.*.*/thegameisover'
```