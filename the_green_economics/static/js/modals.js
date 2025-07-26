class ArticleModal {
    constructor(modalElementId, articlesData) {
        this.modalElement = document.getElementById(modalElementId);
        this.modalTitle = this.modalElement.querySelector("#modal-title");
        this.modalContent = this.modalElement.querySelector("#modal-content");
        this.modalDate = this.modalElement.querySelector("#modal-date");
        this.modalDownloadLink = this.modalElement.querySelector("#modal-download-link");
        this.modalDetailedLink = this.modalElement.querySelector("#modal-detailed-link");
        this.articles = articlesData; // Pass all articles as an array
        this.currentIndex = 0;

        this.closeButton = this.modalElement.querySelector("#modal-close-btn");
        this.prevButton = this.modalElement.querySelector("#modal-prev-btn");
        this.nextButton = this.modalElement.querySelector("#modal-next-btn");

        this.addEventListeners();
    }

    addEventListeners() {
        this.closeButton.addEventListener("click", () => this.close());
        this.modalElement.addEventListener('click', (e) => {
            if (e.target === this.modalElement) this.close();
        });
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') this.close();
        });
        this.prevButton.addEventListener("click", () => this.prev());
        this.nextButton.addEventListener("click", () => this.next());
    }

    updateContent(index) {
        if (index >= 0 && index < this.articles.length) {
            this.currentIndex = index;
            const article = this.articles[this.currentIndex];
            this.modalTitle.textContent = article.title;
            this.modalContent.textContent = article.abstract; // Assuming abstract is the content
            this.modalDate.textContent = `Publicado: ${article.publication_date}`;
            this.modalDownloadLink.setAttribute("href", article.download_url); // Assuming you pass download URL
            this.modalDetailedLink.setAttribute("href", `/articles/${article.slug}`);
        } else {
            console.error("Invalid index");
            this.updateContent(0); // Reset to first article if index is invalid
        }
    }

    open(index) {
        this.updateContent(index);
        this.modalElement.classList.remove("hidden");
        document.body.classList.add("overflow-hidden");
    }

    close() {
        this.modalElement.classList.add("hidden");
        document.body.classList.remove("overflow-hidden");
    }

    prev() {
        if (this.currentIndex > 0) {
            this.updateContent(this.currentIndex - 1);
        }
    }

    next() {
        if (this.currentIndex < this.articles.length - 1) {
            this.updateContent(this.currentIndex + 1);
        }
    }
}


document.addEventListener('DOMContentLoaded', () => {
    // Collect article data from the DOM or better, pass it from Django context as JSON
    const articlesData = [];
    document.querySelectorAll('[data-title]').forEach(articleElement => {
        articlesData.push({
            title: articleElement.dataset.title,
            slug: articleElement.dataset.slug,
            abstract: articleElement.dataset.content, // Assuming content is abstract
            publication_date: articleElement.dataset.date,
            download_url: articleElement.dataset.download
        });
    });

    const articleModal = new ArticleModal('modal', articlesData);

    document.querySelectorAll('.group.cursor-pointer').forEach((articleElement, index) => {
        articleElement.addEventListener('click', () => {
            articleModal.open(index);
        });
    });
});