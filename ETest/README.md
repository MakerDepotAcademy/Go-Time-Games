# Quiz Show

This is the display component of the quiz show

- [Quiz Show](#quiz-show)
  - [Installation](#installation)
  - [Usage](#usage)
    - [GET /](#get)
    - [DELETE /](#delete)
    - [POST /question](#post-question)
    - [POST /answer/:label](#post-answerlabel)
    - [POST /answer/:label/correct](#post-answerlabelcorrect)
    - [POST /start](#post-start)
    - [GET /score](#get-score)
    - [POST /score](#post-score)
    - [POST /score/inc](#post-scoreinc)
    - [POST /score/dec](#post-scoredec)

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

Example:

```bash 
curl -i http://localhost:8080/question -X POST -d 'What is my name'
```

### POST /answer/:label

Set the answer to a question. `:label` must be in `/[a-d]/`

Example:

```bash
curl -i http://localhost:8080/answer/a -X POST -d 'Dan'
```

### POST /answer/:label/correct

Changes the answer of content in `:label` to correct. Halts the round

### POST /start

Starts the round. If this is the first call, will also start game timer

Example:

```bash
curl -i http://localhost:8080/start -X POST
```

### GET /score

Returns the current score

Example:

```bash
curl -i http://localhost:8080/store
```

### POST /score

Sets the score

Example:

```bash
curl -i http://localhost:8080/score -X POST -d '100'
```

### POST /score/inc

Adds to the score

Example:

```bash
curl -i http://localhost:8080/score/inc -X POST -d '10'
```

### POST /score/dec

Subtracts to the score

Example:

```bash
curl -i http://localhost:8080/score/dec -X POST -d '10'
```