const { app, BrowserWindow, ipcMain } = require('electron')
var bodyParser = require('body-parser')
var api = require('express')()
var win
var score = 0, roundTicksLimit = roundTicks = 6, gameTicksLimit = gameTicks = 6 * 60, roundTicker, gameTicker

function updateUI(channel, msg, res) {
  if (win) {
    win.webContents.send(channel, msg);
    res && res.status(200).send('Display updated')
    return true;
  }
  else {
    res && res.status(500).send('Error communicating with render process')
    console.error('No display')
    return false;
  }
}

api.use(bodyParser.urlencoded({ extended: false }))

api.use((req, res, next) => {
  req.body = Object.keys(req.body)[0]
  next()
})

api.use((req, res, next) => {
  if (gameTicks < 1) {
    res.status(401).send('Game over')
  }
  else {
    next()
  }
})

api.get('/', (req, res) => {
  if (win) {
    res.status(200).send('Display is working')
  }
  else {
    res.status(500).send('Display is not working')
  }
})

api.delete('/', (req, res) => {
  app.quit();
  res.status(200).send('Quitting display')
})

api.post('/question', (req, res) => {
  updateUI('question', req.body, res)
})

api.post('/answer/:label', (req, res) => {
  updateUI(req.params.label, req.body, res)
})

api.post('/start', (req, res) => {
  roundTicker = setInterval(() => {
    updateUI('roundtick', roundTicks)
    if (roundTicks-- < 1) {
      updateUI('roundsup', '')
      roundTicks = roundTicksLimit
      clearInterval(roundTicker)
    }
  }, 1000)

  if (!gameTicker) {
    gameTicker = setInterval(() => {
      updateUI('gametick', gameTicks)
      if (gameTicks-- < 1) {
        updateUI('gameover', '')
      }
    }, 1000)
  }

  res.status(200)

  if (gameTicks == gameTicksLimit) {
    res.send('Game started')
  }
  else {
    res.send('Round started')
  }
})

api.post('/answer/:label/correct', (req, res) => {
  clearInterval(roundTicker)
  updateUI(req.param.label + 'correct', 'CORRECT', res)
})

const parseIntBody = (req, res, next) => {
  req.body = parseInt(req.body)
  next()
}

api.post('/score', parseIntBody, (req, res) => {
  score = req.body
  updateUI('score', score, res);
})

api.post('/score/inc', parseIntBody, (req, res) => {
  score += req.body
  updateUI('score', score, res);
})

api.post('/score/dec', parseIntBody, (req, res) => {
  score -= req.body
  updateUI('score', score, res);
})

api.get('/score', (req, res) => {
  if (win) {
    ipcMain.once('score', (evt, arg) => {
      res.status(200).send(arg)
    })
    win.webContents.send('score', 'give')
  }
  else {
    res.status(500).send('No display')
  }
})

app.on('ready', () => {
  // Create the browser window.
  win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true
    }
  })

  win.loadFile('app/index.html')
  win.on('closed', () => {
    win = null
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

api.listen(8080, '0.0.0.0')