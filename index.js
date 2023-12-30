const express = require('express')
const app = express()
const util = require('util');
const exec = util.promisify(require('child_process').exec);
const cors = require('cors');

async function makeMusic(text) {
  const command = `python melody.py --text "${text}" --outfile_name "outputs/new_request"`
  const { stdout, stderr } = await exec(command)

  //console.log('stdout:', stdout);
  //console.error('stderr:', stderr);
}

app.use(cors())
app.use('/music', express.static('outputs'))

app.get('/api/musicgen', async (req, res) => {
  console.log(`params text=${req.query.text}`)
  await makeMusic(req.query.text)
  res.send("Your song completed!")
});

PORT = process.env.port || 3000
app.listen(PORT, () => console.log(`Listening on PORT=${PORT}`))
