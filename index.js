const express = require('express')
const app = express()
const util = require('util');
const exec = util.promisify(require('child_process').exec);
const cors = require('cors');
const uuidv4 = require('uuid').v4;

async function makeMusic(text) {
  const name = uuidv4();
  const command = `python melody.py --text "${text}" --name ${name}`
  console.log(`Running command: ${command}`)
  return name;
  //const { stdout, stderr } = await exec(command)
}

app.use(cors())
app.use('/music', express.static('outputs'))

app.get('/api/musicgen', async (req, res) => {
  console.log(`params text=${req.query.text}`)
  const new_riff = await makeMusic(req.query.text)
  res.send(`/music/${new_riff}.wav`)
});

PORT = process.env.port || 8000
app.listen(PORT, () => console.log(`Listening on PORT=${PORT}`))
