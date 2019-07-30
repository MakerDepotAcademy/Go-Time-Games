const { app, BrowserWindow, ipcMain } = require('electron')
var bodyParser = require('body-parser')
var api = require('express')()
var win
var score, roundTicks, gameTicks

function updateUI(channel, msg, res) {
  if (win) {
    win.webContents.send(channel, msg);
    res.status(200).send('Display updated')
    return true;
  }
  else {
    res.status(500).send('Error communicating with render process')
    console.error('No display')
    return false;
  }
}

api.use(bodyParser.urlencoded({ extended: false }))
api.use(bodyParser.json())

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
  updateUI(req.param.label, req.body, res)
})

api.post('/start', (req, res) => {

})

api.post('/answer/:label/correct', (req, res) => {
  updateUI(req.param.label + 'correct', 'CORRECT', res)
})

api.post('/score', (req, res) => {
  score = req.body
  updateUI('score', score, res);
})

api.post('/score/inc', (req, res) => {
  score += req.body
  updateUI('score', score, res);
})

api.post('/score/dec', (req, res) => {
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