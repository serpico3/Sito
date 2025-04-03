// Funzione per attivare le animazioni quando gli elementi sono visibili
const animateOnScroll = function() {
    const elements = document.querySelectorAll('.animate-on-scroll');
    
    elements.forEach(element => {
        const elementPosition = element.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;
        
        if (elementPosition < windowHeight - 100) {
            element.classList.add('animate__animated', 'animate__fadeIn');
        }
    });
};

// Gestione modali progetti
const setupProjectModals = function() {
    // Apertura modale
    document.querySelectorAll('.project-card').forEach(card => {
        card.addEventListener('click', function(e) {
            // Evita l'apertura se si clicca su un link
            if (e.target.tagName === 'A' || e.target.closest('a')) return;
            
            const projectId = this.getAttribute('data-project');
            const modal = document.getElementById(`modal-${projectId}`);
            if (modal) {
                modal.style.display = "block";
                document.body.style.overflow = "hidden";
            }
        });
    });

    // Chiusura modale
    document.querySelectorAll('.close-modal').forEach(btn => {
        btn.addEventListener('click', function() {
            this.closest('.project-modal').style.display = "none";
            document.body.style.overflow = "auto";
        });
    });

    // Chiusura cliccando fuori dal modal
    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('project-modal')) {
            e.target.style.display = "none";
            document.body.style.overflow = "auto";
        }
    });
};

// Smooth scroll per i link interni
const setupSmoothScroll = function() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
};

// Esegui al caricamento della pagina
document.addEventListener('DOMContentLoaded', function() {
    animateOnScroll();
    setupProjectModals();
    setupSmoothScroll();
    
    window.addEventListener('scroll', animateOnScroll);
});

// Aggiungi queste funzioni alla fine del file esistente

function setupPhotographyGallery() {
    // Gestione click sulle cartelle
    document.querySelectorAll('.gallery-folder').forEach(folder => {
        folder.addEventListener('click', function(e) {
            if (e.target.classList.contains('download-folder')) return;
            
            const folderId = this.getAttribute('data-folder');
            openLightbox(folderId);
        });
    });

    // Gestione download cartelle
    document.querySelectorAll('.download-folder').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const folderId = this.closest('.gallery-folder').getAttribute('data-folder');
            downloadFolder(folderId);
        });
    });

    // Gestione lightbox
    document.querySelector('.lightbox-close').addEventListener('click', closeLightbox);
    document.querySelector('.lightbox-prev').addEventListener('click', prevPhoto);
    document.querySelector('.lightbox-next').addEventListener('click', nextPhoto);
    document.querySelector('.lightbox-download').addEventListener('click', downloadCurrentPhoto);
}

let currentPhotos = [];
let currentIndex = 0;

// Oggetto per definire i dettagli di ogni cartella
const folderDetails = {
    'praga': {
        title: 'praga',
        count: 2, // Numero di foto nella cartella
        photos: []  // Verrà riempito dinamicamente
    }
};

function openLightbox(folderId) {
    const folder = folderDetails[folderId];
    if (!folder) return;
    
    // In un'app reale, qui faresti una chiamata AJAX
    // Per ora, generiamo dinamicamente i percorsi delle immagini
    currentPhotos = [];
    
    // Genera i percorsi delle foto in base al conteggio nella cartella
    for (let i = 1; i <= folder.count; i++) {
        currentPhotos.push({
            url: `assets/images/folders/${folderId}/${i}.jpg`,
            title: `${folder.title} - Foto ${i}`
        });
    }
    
    currentIndex = 0;
    updateLightbox();
    document.getElementById('lightbox').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    document.getElementById('lightbox').style.display = 'none';
    document.body.style.overflow = 'auto';
}

function updateLightbox() {
    if (currentPhotos.length === 0) return;
    
    const lightbox = document.getElementById('lightbox');
    lightbox.querySelector('.lightbox-img').src = currentPhotos[currentIndex].url;
    lightbox.querySelector('.lightbox-img').alt = currentPhotos[currentIndex].title;
    lightbox.querySelector('.lightbox-title').textContent = currentPhotos[currentIndex].title;
    lightbox.querySelector('.lightbox-counter').textContent = `${currentIndex + 1}/${currentPhotos.length}`;
}

function nextPhoto() {
    if (currentPhotos.length === 0) return;
    currentIndex = (currentIndex + 1) % currentPhotos.length;
    updateLightbox();
}

function prevPhoto() {
    if (currentPhotos.length === 0) return;
    currentIndex = (currentIndex - 1 + currentPhotos.length) % currentPhotos.length;
    updateLightbox();
}

function downloadFolder(folderId) {
    // Simulazione download (in un'app reale sarebbe una chiamata al server)
    console.log(`Download folder ${folderId} initiated`);
    // Qui implementeresti la logica per scaricare l'intera cartella come ZIP
}

function downloadCurrentPhoto() {
    if (currentPhotos.length === 0) return;
    
    const link = document.createElement('a');
    link.href = currentPhotos[currentIndex].url;
    link.download = `photo-${currentIndex + 1}.jpg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Aggiorna l'evento DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    animateOnScroll();
    setupProjectModals();
    setupSmoothScroll();
    setupPhotographyGallery(); // Aggiungi questa linea
    
    window.addEventListener('scroll', animateOnScroll);
});