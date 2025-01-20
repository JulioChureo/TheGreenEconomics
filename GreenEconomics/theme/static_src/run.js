// run.js (dentro de theme/static_src)
const { exec } = require('child_process');

// Usamos el comando de npm run dev para empezar la compilación de Tailwind en modo desarrollo
exec('npm run dev', (error, stdout, stderr) => {
  if (error) {
    console.error(`Error al ejecutar el comando: ${error}`);
    return;
  }
  if (stderr) {
    console.error(`stderr: ${stderr}`);
    return;
  }
  console.log(`stdout: ${stdout}`);
});