const util = require('util');
const exec = util.promisify(require('child_process').exec);

async function makeMusic() {
  const command = 'python melody.py --text "lofi girl" --outfile_name "lofi_girl"'
  const { stdout, stderr } = await exec(command)

  console.log('stdout:', stdout);
  console.error('stderr:', stderr);
}

makeMusic()
