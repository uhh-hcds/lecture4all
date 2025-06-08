// Apply the switch state as soon as possible to avoid flicker
(function () {
    const savedState = localStorage.getItem("shortsSwitch");
    const isChecked = savedState === "true";
    const switchElement = document.getElementById("shorts");
    if (switchElement) {
        switchElement.checked = isChecked;
        switchElement.classList.remove("hidden"); // Remove the hidden class
    }
})();

document.addEventListener("DOMContentLoaded", function () {
    const switchElement = document.getElementById("shorts");
    const textElement = document.getElementById("shortsViewInfo");
    const searchForm = document.getElementById("searchForm");

    // Function to update the visibility of the paragraph
    function updateShortsViewInfo(isChecked) {
        if (textElement) {
            textElement.style.display = isChecked ? "block" : "none";
        }
        updateFormAction(isChecked); // Update the form action
    }

    // Function to update the form action
    function updateFormAction(isChecked) {
        if (searchForm) {
            const shortsUrl = searchForm.getAttribute('data-shorts-url');
            const searchResultsUrl = searchForm.getAttribute('data-searchresults-url');
            searchForm.action = isChecked ? shortsUrl : searchResultsUrl;
        }
    }

    // Load saved state from localStorage
    const savedState = localStorage.getItem("shortsSwitch");
    const isChecked = savedState === "true";
    if (switchElement) {
        switchElement.checked = isChecked;
        updateShortsViewInfo(isChecked);

        // Event listener to toggle visibility and save state
        switchElement.addEventListener("change", function () {
            localStorage.setItem("shortsSwitch", switchElement.checked);
            updateShortsViewInfo(switchElement.checked);
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const microButton = document.getElementById('micro-btn');
    const fertig = document.querySelector(".roundButton");
    const schließen = document.getElementById('schließen');
    const audioPopup = document.getElementById('audioPopup');
    const searchForm = document.getElementById('searchForm');
    const loadingPopup = document.getElementById('loadingPopup');
    const warningDiv = document.getElementById('speech-recognition-warning');

    let stream;
    let recorder;

    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        warningDiv.style.display = 'block';
    } else {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'de-DE';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        microButton.addEventListener("click", async () => {
            stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            recorder = new MediaRecorder(stream);
            audioPopup.style.display = 'flex';
            recognition.start();
        });

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            console.log('Erkanntes Wort:', transcript);
            document.querySelector('input[name="query"]').value = transcript;
            document.getElementById('searchForm').submit();
        };

        recognition.onerror = (event) => {
            console.error('Fehler bei der Spracherkennung:', event.error);
        };

        recognition.onend = () => {
            console.log('Spracherkennung beendet.');
        };

        fertig.addEventListener('click', () => {
            stream.getTracks().forEach(track => track.stop());
            recognition.stop();
        });

        schließen.addEventListener("click", () => {
            stream.getTracks().forEach(track => track.stop());
            recognition.stop();
            audioPopup.style.display = 'none';
        });

        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                stream.getTracks().forEach(track => track.stop());
                recognition.stop();
                audioPopup.style.display = 'none';
            }
        });
    }


    searchForm.addEventListener('submit', function(event) {
        event.preventDefault(); 
        loadingPopup.style.display = 'flex';
        setTimeout(function() {
            searchForm.submit(); // Submit the form after 3 seconds
        }, 1000);
    });
});
function changePlaceholder(text) {
    document.getElementById('query').placeholder = text;
}

// Video view:
function createVideoCard(video, videolink) {

    const colDiv = document.createElement('div');
    colDiv.classList.add('col', 'mb-4');

    const cardDiv = document.createElement('div');
    cardDiv.classList.add('card');

    // Erstelle den Link (a-Element)
    const link = document.createElement('a');
    link.href = videolink;

    const img = document.createElement('img');
    img.src = video.thumbnail_url;
    img.alt = 'video';
    img.classList.add('card-img-top');
    link.appendChild(img);

    const cardBodyDiv = document.createElement('div');
    cardBodyDiv.classList.add('card-body');

    const title = document.createElement('h5');
    title.classList.add('card-title');
    title.textContent = shortenTextIfNecessary(video.title, 70);

    const speaker = document.createElement('p');
    speaker.classList.add('card-text');
    speaker.id = 'vspeaker';
    speaker.textContent = video.speaker;

    const date = document.createElement('p');
    date.classList.add('card-text');
    const dateSmall = document.createElement('small');
    dateSmall.classList.add('text-muted');
    dateSmall.textContent = video.date;
    date.appendChild(dateSmall);

    cardBodyDiv.appendChild(title);
    cardBodyDiv.appendChild(speaker);
    cardBodyDiv.appendChild(date);

    cardDiv.appendChild(link);
    cardDiv.appendChild(cardBodyDiv);

    colDiv.appendChild(cardDiv);

    return colDiv;
}
function shortenTextIfNecessary(text, maxLength) {
    if (text.length > maxLength) {
        return text.slice(0, maxLength - 2) + '...';
    }
    return text;
}