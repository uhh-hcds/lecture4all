const short = document.getElementById('currentShort');
const metaDaten = document.querySelector('.meta-daten');
const videoButton = document.getElementById('videoButton');
const sideboard = document.querySelector('.sideboard');
const resultsJS = getResultsJS();
const seekBar = document.getElementById('seek-bar-shorts');
seekBar.style.setProperty('--progress', 0);

    document.getElementById('right').addEventListener('click', skipVideo);
    document.getElementById('left').addEventListener('click', videoBack);
    // Konfiguration

    const chunks = resultsJS.flatMap(video =>
        video.chunks.map(chunk => ({
            url: video.m3u8_url,
            videoId: video.video_id,
            title: video.title,
            speaker: video.speaker,
            date: video.date,
            text: chunk.text,
            rank: chunk.chunk_rank,
            start: chunk.start,
            end: chunk.end
        }))
    );

    // Chunks nach Rank sortieren
    const sortedChunks = chunks.sort((a, b) => a.rank - b.rank);

    let currentIndex = 0;

    function changeSrc(videoUrl) 
    {
        if (short.canPlayType('application/vnd.apple.mpegurl')) {
            short.src = videoUrl;
        } else if (Hls.isSupported()) {
            const hls = new Hls();
            hls.loadSource(videoUrl);
            hls.attachMedia(short);
            hls.on(Hls.Events.MANIFEST_PARSED, function() {
                // auszuführen wenn geladen evtl loadedmetadata hier rein
            });
        } else {
            alert('Dein Browser unterstützt leider keine Wiedergabe von HLS-Streams.');
        }
    }

    // Aktualisieren des Iframes und Sideboards
    function updateUI(index) {
        const chunk = sortedChunks[index];
        changeSrc(chunk.url);
        short.currentTime = chunk.start;
        metaDaten.innerHTML = `<h5>${chunk.title}</h5><p>${chunk.speaker} <br> ${chunk.date}</p>`;
        videoButton.href = `${getVideoUrl()}?video_id=${chunk.videoId}`;
        sideboard.innerHTML = `<h3>${shortenTextIfNecessary(chunk.title, 50)}</h3><p>...${chunk.text}...</p>`;
    }
    updateUI(0);

    function skipVideo() {
        if (currentIndex < sortedChunks.length - 1) {
            currentIndex++;
            updateUI(currentIndex);
        }
    }

    function videoBack() {
        if (currentIndex > 0) {
            currentIndex--;
            updateUI(currentIndex);
        }
    }

    short.addEventListener('timeupdate', () => {
        if(short.currentTime >= sortedChunks[currentIndex].end)
        {
            skipVideo();
        }
        const progress = ((short.currentTime - sortedChunks[currentIndex].start) / (sortedChunks[currentIndex].end - sortedChunks[currentIndex].start)) * 100;
        seekBar.style.setProperty('--progress', `${progress}%`);
        
    });
    short.addEventListener('click', () => {
        if (short.paused) {
            short.play();
        } else {
            short.pause();
        }
    });
    

    // Mobileview
    const MOVE_THRESHOLD = 100;

    let initialX = 0;
    let moveX = 0;
    let isDeleteButtonOpen = false;

    document.addEventListener("touchstart", e => {
        initialX = e.touches[0].pageX;
    });
    document.addEventListener("touchmove", e => {
        let currentX = e.touches[0].pageX;
        moveX = currentX - initialX;
    });
    document.addEventListener("touchend", e => {
        if (moveX < MOVE_THRESHOLD * (-1)) {
            // Swipe right
            skipVideo();
        } else if (moveX > MOVE_THRESHOLD ) {
            // Swipe left
            videoBack();
        }

        moveX = 0;
    });
