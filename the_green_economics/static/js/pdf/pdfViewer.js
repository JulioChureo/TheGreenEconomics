import pdfjsDist from 'https://cdn.jsdelivr.net/npm/pdfjs-dist@5.1.91/+esm'
var { pdfjsLib } = globalThis;

pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdn.jsdelivr.net/npm/pdfjs-dist@5.1.91/build/pdf.worker.mjs';

/* ---------- lógica de escala ---------- */
function isFullscreen() {
  return !!(
    document.fullscreenElement ||
    document.webkitFullscreenElement ||
    document.mozFullScreenElement ||
    document.msFullscreenElement
  );
}

function adjustScale() {
  return isFullscreen() ? 1.4 : 1.0;
}

var isAdjustingScale = false;
var pdf, viewport;
var scale = adjustScale();
var pageNumber = 1;

// elements
const prevButton = document.getElementById('prev');
const nextButton = document.getElementById('next');
const fullScreenButton = document.getElementById('fullScreen');
const headerVisibilitySpacer = document.getElementById('headerVisibilitySpacer');
const scaleSlider = document.getElementById('scale');
const pageNum = document.getElementById('page_num');
const BoookUrl = document.getElementById('the-canvas').getAttribute('pdf-url');

// canvas setup
const canvas = document.getElementById('the-canvas');
const context = canvas.getContext('2d');
canvas.height = 650;
canvas.width = 450;

// function declarations
var renderPage = async (pageNumber) => {}

fullScreenButton.addEventListener('click', function() {
  if (!isFullscreen()) {
    headerVisibilitySpacer.style.display = 'none';
    const docElm = document.documentElement;
    if (docElm.requestFullscreen) {
      docElm.requestFullscreen();
    } else if (docElm.mozRequestFullScreen) { /* Firefox */
      docElm.mozRequestFullScreen();
    } else if (docElm.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
      docElm.webkitRequestFullscreen();
    } else if (docElm.msRequestFullscreen) { /* IE/Edge */
      docElm.msRequestFullscreen();
    }
  } else {
    headerVisibilitySpacer.style.display = 'block';
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.mozCancelFullScreen) { /* Firefox */
      document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) { /* Chrome, Safari and Opera */
      document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) { /* IE/Edge */
      document.msExitFullscreen();
    }
  }
});

scaleSlider.addEventListener('input', async function() {
  isAdjustingScale = true;
  scale = parseFloat(this.value);
  console.log('Scale changed via slider. New scale:', scale);
  await renderPage(pageNumber); 
});

async function onFullscreenChange() {
    if (isAdjustingScale) {
        isAdjustingScale = false;
        return;
    }
    const newScale = adjustScale();
    scaleSlider.value = newScale;
    console.log('Fullscreen changed. New scale:', newScale, 'Old scale:', scale);
    scale = newScale;
    await renderPage(pageNumber); 
}



document.addEventListener('fullscreenchange', async function() {
  await onFullscreenChange();
});

// event listeners
prevButton.addEventListener('click', function() {
    if (pageNumber > 1) {
        pageNumber -= 1;
        renderPage(pageNumber).then(() => {
            pageNum.innerText = pageNumber + '/' + pdf.numPages;
        });
    }
});

nextButton.addEventListener('click', async function() {
    if (pageNumber < pdf.numPages) {
        pageNumber += 1;
        renderPage(pageNumber).then(() => {
            pageNum.innerText = pageNumber + '/' + pdf.numPages;
        });
    }
});


// entry point
var loadingTask = pdfjsLib.getDocument(BoookUrl);
//var pdf = await loadingTask.promise;
loadingTask.promise.then(function(pdfPromise) {
    pdf = pdfPromise;
    renderPage = async function(pageNumber) {
        let page = await pdf.getPage(pageNumber)
        viewport = page.getViewport({scale: scale});
        console.log(viewport);
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        const renderContext = {
            canvasContext: context,
            viewport: viewport
        };
        await page.render(renderContext).promise;
    }

    renderPage(pageNumber).then(() => {
        pageNum.innerText = pageNumber + '/' + pdf.numPages;
    }
    ).catch((error) => {
        console.error('Error rendering page:', error);
    });
});




