const express = require('express')
const app = express()
const util = require('util');
const exec = util.promisify(require('child_process').exec);

async function makeMusic(text) {
  const command = `python melody.py --text "${text}" --outfile_name "outputs/new_request"`
  const { stdout, stderr } = await exec(command)

  //console.log('stdout:', stdout);
  //console.error('stderr:', stderr);
}

//makeMusic()

PORT = 3000

app.use(express.static('outputs'))

app.get('/api/musicgen', async (req, res) => {
  console.log(`parmas text=${req.query.text}`)
  await makeMusic(req.query.text)
  res.send("Your song completed!")
});

app.listen(PORT, () => console.log(`Listening on PORT=${PORT}`))
