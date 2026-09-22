let DATA = null;
let CURRENT_VIEW = "overview";

const $ = selector => document.querySelector(selector);

const formatNumber = value =>
    new Intl.NumberFormat("en-IN").format(Number(value || 0));

const formatPercent = value =>
    `${(Number(value || 0) * 100).toFixed(1)}%`;

const escapeHTML = value =>
    String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");

function statusClass(status) {
    const value = String(status || "").toLowerCase();

    if (
        value.includes("complete") ||
        value.includes("published")
    ) {
        return "badge-success";
    }

    if (
        value.includes("progress") ||
        value.includes("writing") ||
        value.includes("editing")
    ) {
        return "badge-warning";
    }

    if (
        value.includes("not started") ||
        value.includes("pending")
    ) {
        return "badge-neutral";
    }

    return "badge-neutral";
}

function badge(status) {
    return `
        <span class="badge ${statusClass(status)}">
            ${escapeHTML(status || "Unknown")}
        </span>
    `;
}

function progressBar(value) {
    const percent = Math.max(
        0,
        Math.min(100, Number(value || 0) * 100)
    );

    return `
        <div class="progress-track">
            <div
                class="progress-fill"
                style="width:${percent}%"
            ></div>
        </div>
    `;
}

function getBook(id) {
    return DATA.books.find(book => book.id === id);
}

function setView(view) {
    CURRENT_VIEW = view;

    document.querySelectorAll(".nav-item").forEach(item => {
        item.classList.toggle(
            "active",
            item.dataset.view === view
        );
    });

    const titles = {
        overview: "Command Center",
        categories: "Category Intelligence",
        books: "Book Library",
        chapters: "Chapter Control",
        pipeline: "Publishing Pipeline",
        analytics: "Publishing Analytics",
        attention: "Needs Attention"
    };

    $("#viewTitle").textContent =
        titles[view] || "Command Center";

    render();
}

function render() {
    if (!DATA) return;

    const views = {
        overview: renderOverview,
        categories: renderCategories,
        books: renderBooks,
        chapters: renderChapters,
        pipeline: renderPipeline,
        analytics: renderAnalytics,
        attention: renderAttention
    };

    (views[CURRENT_VIEW] || renderOverview)();
}

function renderOverview() {
    const s = DATA.summary;

    const categories = [...DATA.categories]
        .sort((a, b) => b.completion - a.completion)
        .slice(0, 10);

    const statuses = s.book_statuses || {};

    const completed =
        Object.entries(statuses)
            .filter(([key]) =>
                key.toLowerCase().includes("complete")
            )
            .reduce((sum, [, value]) => sum + value, 0);

    const inProgress =
        Object.entries(statuses)
            .filter(([key]) =>
                key.toLowerCase().includes("progress")
            )
            .reduce((sum, [, value]) => sum + value, 0);

    const notStarted =
        Object.entries(statuses)
            .filter(([key]) =>
                key.toLowerCase().includes("not started")
            )
            .reduce((sum, [, value]) => sum + value, 0);

    $("#content").innerHTML = `

        <div class="page-head">
            <div>
                <div class="eyebrow">Digital Publishing Operations</div>
                <h1>Your publishing universe.</h1>
                <p>
                    A repository-driven command center connecting
                    categories, books, chapters, writing progress,
                    research and publishing operations.
                </p>
            </div>

            <div class="generated">
                DATA GENERATED<br>
                ${escapeHTML(DATA.generated_at)}
            </div>
        </div>

        <div class="kpi-grid">

            <div class="kpi">
                <div class="kpi-label">Total Books</div>
                <div class="kpi-value">
                    ${formatNumber(s.total_books)}
                </div>
                <div class="kpi-meta">
                    Across ${formatNumber(s.total_categories)} categories
                </div>
            </div>

            <div class="kpi">
                <div class="kpi-label">Total Chapters</div>
                <div class="kpi-value">
                    ${formatNumber(s.total_chapters)}
                </div>
                <div class="kpi-meta">
                    ${formatNumber(s.completed_chapters)}
                    completed
                </div>
            </div>

            <div class="kpi">
                <div class="kpi-label">Words Written</div>
                <div class="kpi-value">
                    ${formatNumber(s.total_words)}
                </div>
                <div class="kpi-meta">
                    Target ${formatNumber(s.target_words)}
                </div>
            </div>

            <div class="kpi">
                <div class="kpi-label">Average Completion</div>
                <div class="kpi-value">
                    ${formatPercent(s.average_completion)}
                </div>
                <div class="kpi-meta">
                    Across the complete book portfolio
                </div>
            </div>

        </div>

        <div class="dashboard-grid">

            <div class="panel">
                <div class="panel-header">
                    <h2>Category Performance</h2>
                    <span>Top 10 by completion</span>
                </div>

                <div class="panel-body">
                    <div class="category-list">

                        ${categories.map(category => `

                            <div
                                class="category-row"
                                onclick="openCategory('${encodeURIComponent(category.name)}')"
                            >

                                <div class="category-top">

                                    <span class="category-name">
                                        ${escapeHTML(category.name)}
                                    </span>

                                    <span class="category-value">
                                        ${formatPercent(category.completion)}
                                        · ${category.books} books
                                    </span>

                                </div>

                                ${progressBar(category.completion)}

                            </div>

                        `).join("")}

                    </div>
                </div>
            </div>

            <div class="panel">

                <div class="panel-header">
                    <h2>Portfolio Status</h2>
                    <span>Book status distribution</span>
                </div>

                <div class="panel-body">

                    <div class="status-grid">

                        <div class="status-box status-complete">
                            <strong>${completed}</strong>
                            <span>Completed</span>
                        </div>

                        <div class="status-box status-progress">
                            <strong>${inProgress}</strong>
                            <span>In Progress</span>
                        </div>

                        <div class="status-box status-start">
                            <strong>${notStarted}</strong>
                            <span>Not Started</span>
                        </div>

                    </div>

                    <div style="height:18px"></div>

                    <h2 style="font-size:11px;margin:0 0 10px">
                        Chapter Status
                    </h2>

                    ${Object.entries(s.chapter_statuses || {})
                        .map(([status, count]) => `
                            <div class="category-top" style="margin-top:10px">
                                <span class="category-name">
                                    ${escapeHTML(status)}
                                </span>
                                <span class="category-value">
                                    ${formatNumber(count)}
                                </span>
                            </div>
                        `).join("")}

                </div>
            </div>

        </div>

        <div class="panel">

            <div class="panel-header">
                <h2>Book Portfolio</h2>
                <span>${formatNumber(s.total_books)} books</span>
            </div>

            <div class="panel-body">

                <div class="search-row">

                    <input
                        id="overviewSearch"
                        class="search-input"
                        placeholder="Search books, IDs or categories..."
                    >

                    <select id="overviewCategory" class="filter-select">
                        <option value="">All categories</option>
                        ${DATA.categories.map(category => `
                            <option value="${escapeHTML(category.name)}">
                                ${escapeHTML(category.name)}
                            </option>
                        `).join("")}
                    </select>

                </div>

                <div id="overviewBooks"></div>

            </div>
        </div>
    `;

    const renderOverviewBooks = () => {

        const search =
            ($("#overviewSearch")?.value || "")
                .toLowerCase();

        const category =
            $("#overviewCategory")?.value || "";

        const books = DATA.books
            .filter(book => {

                const matchesSearch =
                    !search ||
                    book.title.toLowerCase().includes(search) ||
                    book.id.toLowerCase().includes(search) ||
                    book.category.toLowerCase().includes(search);

                const matchesCategory =
                    !category ||
                    book.category === category;

                return matchesSearch && matchesCategory;
            })
            .slice(0, 12);

        $("#overviewBooks").innerHTML = `
            <div class="card-grid">
                ${books.map(bookCard).join("")}
            </div>
        `;
    };

    $("#overviewSearch").addEventListener(
        "input",
        renderOverviewBooks
    );

    $("#overviewCategory").addEventListener(
        "change",
        renderOverviewBooks
    );

    renderOverviewBooks();
}

function bookCard(book) {

    return `
        <div
            class="book-card"
            onclick="openBook('${encodeURIComponent(book.id)}')"
        >

            <div class="book-id">
                ${escapeHTML(book.id)}
            </div>

            <h3>${escapeHTML(book.title)}</h3>

            <div class="book-category">
                ${escapeHTML(book.category)}
            </div>

            ${progressBar(book.completion)}

            <div class="book-stats">

                <div class="book-stat">
                    <strong>${formatPercent(book.completion)}</strong>
                    <span>Progress</span>
                </div>

                <div class="book-stat">
                    <strong>${formatNumber(book.chapters.actual)}</strong>
                    <span>Chapters</span>
                </div>

                <div class="book-stat">
                    <strong>${formatNumber(book.words.current)}</strong>
                    <span>Words</span>
                </div>

            </div>

        </div>
    `;
}

function renderCategories() {

    $("#content").innerHTML = `

        <div class="page-head">
            <div>
                <div class="eyebrow">Portfolio Structure</div>
                <h1>Categories.</h1>
                <p>
                    Explore your publishing portfolio by subject,
                    book volume, chapter volume and progress.
                </p>
            </div>
        </div>

        <div class="card-grid">

            ${DATA.categories.map(category => `

                <div
                    class="book-card"
                    onclick="openCategory('${encodeURIComponent(category.name)}')"
                >

                    <div class="book-id">
                        CATEGORY
                    </div>

                    <h3>${escapeHTML(category.name)}</h3>

                    <div class="book-category">
                        ${category.books} books ·
                        ${category.chapters} chapters
                    </div>

                    ${progressBar(category.completion)}

                    <div class="book-stats">

                        <div class="book-stat">
                            <strong>
                                ${formatPercent(category.completion)}
                            </strong>
                            <span>Progress</span>
                        </div>

                        <div class="book-stat">
                            <strong>
                                ${formatNumber(category.words)}
                            </strong>
                            <span>Words</span>
                        </div>

                        <div class="book-stat">
                            <strong>
                                ${formatNumber(category.completed_chapters)}
                            </strong>
                            <span>Completed</span>
                        </div>

                    </div>

                </div>

            `).join("")}

        </div>
    `;
}

function renderBooks() {

    $("#content").innerHTML = `

        <div class="page-head">
            <div>
                <div class="eyebrow">Book Portfolio</div>
                <h1>Books.</h1>
                <p>
                    Search and inspect every book connected to
                    the repository tracker.
                </p>
            </div>
        </div>

        <div class="panel">

            <div class="panel-body">

                <div class="search-row">

                    <input
                        id="bookSearch"
                        class="search-input"
                        placeholder="Search by title, ID or category..."
                    >

                    <select id="bookCategory" class="filter-select">
                        <option value="">All categories</option>

                        ${DATA.categories.map(category => `
                            <option value="${escapeHTML(category.name)}">
                                ${escapeHTML(category.name)}
                            </option>
                        `).join("")}

                    </select>

                </div>

                <div id="bookResults" class="card-grid"></div>

            </div>
        </div>
    `;

    const update = () => {

        const search =
            $("#bookSearch").value.toLowerCase();

        const category =
            $("#bookCategory").value;

        const books = DATA.books.filter(book => {

            const matchesSearch =
                !search ||
                book.title.toLowerCase().includes(search) ||
                book.id.toLowerCase().includes(search) ||
                book.category.toLowerCase().includes(search);

            const matchesCategory =
                !category ||
                book.category === category;

            return matchesSearch && matchesCategory;
        });

        $("#bookResults").innerHTML =
            books.length
                ? books.map(bookCard).join("")
                : `
                    <div class="empty-state">
                        <strong>No books found</strong>
                        Try another search or category.
                    </div>
                `;
    };

    $("#bookSearch").addEventListener("input", update);
    $("#bookCategory").addEventListener("change", update);

    update();
}

function renderChapters() {

    const chapters = DATA.books.flatMap(book =>
        book.chapters_data.map(chapter => ({
            ...chapter,
            book
        }))
    );

    $("#content").innerHTML = `

        <div class="page-head">
            <div>
                <div class="eyebrow">Content Operations</div>
                <h1>Chapters.</h1>
                <p>
                    Repository-level chapter inventory across
                    the complete book portfolio.
                </p>
            </div>
        </div>

        <div class="panel">

            <div class="panel-body">

                <div class="search-row">

                    <input
                        id="chapterSearch"
                        class="search-input"
                        placeholder="Search chapter, book or category..."
                    >

                    <select id="chapterStatus" class="filter-select">

                        <option value="">All statuses</option>
                        <option>Completed</option>
                        <option>In Progress</option>
                        <option>Started</option>
                        <option>Not Started</option>

                    </select>

                </div>

                <div class="table-wrap">

                    <table class="data-table">

                        <thead>
                            <tr>
                                <th>Chapter</th>
                                <th>Book</th>
                                <th>Category</th>
                                <th>Words</th>
                                <th>Status</th>
                            </tr>
                        </thead>

                        <tbody id="chapterResults"></tbody>

                    </table>

                </div>

            </div>
        </div>
    `;

    const update = () => {

        const search =
            $("#chapterSearch").value.toLowerCase();

        const status =
            $("#chapterStatus").value;

        const filtered = chapters.filter(item => {

            const matchesSearch =
                !search ||
                item.title.toLowerCase().includes(search) ||
                item.book.title.toLowerCase().includes(search) ||
                item.book.category.toLowerCase().includes(search);

            const matchesStatus =
                !status ||
                item.status === status;

            return matchesSearch && matchesStatus;
        });

        $("#chapterResults").innerHTML =
            filtered.map(item => `

                <tr>

                    <td>
                        <strong>
                            Chapter ${item.number}
                        </strong>
                    </td>

                    <td>
                        <span
                            class="book-link"
                            onclick="openBook('${encodeURIComponent(item.book.id)}')"
                        >
                            ${escapeHTML(item.book.title)}
                        </span>
                    </td>

                    <td>
                        ${escapeHTML(item.book.category)}
                    </td>

                    <td>
                        ${formatNumber(item.words)}
                    </td>

                    <td>
                        ${badge(item.status)}
                    </td>

                </tr>

            `).join("");

    };

    $("#chapterSearch").addEventListener("input", update);
    $("#chapterStatus").addEventListener("change", update);

    update();
}

function renderPipeline() {

    $("#content").innerHTML = `

        <div class="page-head">
            <div>
                <div class="eyebrow">Production Workflow</div>
                <h1>Publishing pipeline.</h1>
                <p>
                    Track research, writing, editing and publishing
                    activity across the entire portfolio.
                </p>
            </div>
        </div>

        <div class="pipeline">

            ${DATA.pipeline.map(stage => {

                const total =
                    Object.values(stage.counts)
                        .reduce((a,b) => a+b, 0);

                return `

                    <div class="pipeline-stage">

                        <h3>
                            ${escapeHTML(stage.stage)}
                        </h3>

                        <div class="pipeline-total">
                            ${total} books
                        </div>

                        <div class="pipeline-bars">

                            ${Object.entries(stage.counts)
                                .map(([status, count]) => `

                                    <div>

                                        <div class="pipeline-bar">
                                            <span>
                                                ${escapeHTML(status)}
                                            </span>

                                            <strong>
                                                ${count}
                                            </strong>
                                        </div>

                                        ${progressBar(
                                            total ? count / total : 0
                                        )}

                                    </div>

                                `).join("")}

                        </div>

                    </div>
                `;
            }).join("")}

        </div>

        <div style="height:16px"></div>

        <div class="panel">

            <div class="panel-header">
                <h2>Book Pipeline Matrix</h2>
                <span>Research → Writing → Editing → Publishing</span>
            </div>

            <div class="table-wrap">

                <table class="data-table">

                    <thead>
                        <tr>
                            <th>Book</th>
                            <th>Research</th>
                            <th>Writing</th>
                            <th>Editing</th>
                            <th>Publishing</th>
                            <th>Progress</th>
                        </tr>
                    </thead>

                    <tbody>

                        ${DATA.books.map(book => `

                            <tr>

                                <td>
                                    <span
                                        class="book-link"
                                        onclick="openBook('${encodeURIComponent(book.id)}')"
                                    >
                                        ${escapeHTML(book.title)}
                                    </span>
                                </td>

                                <td>${badge(book.pipeline.research)}</td>
                                <td>${badge(book.pipeline.writing)}</td>
                                <td>${badge(book.pipeline.editing)}</td>
                                <td>${badge(book.pipeline.publishing)}</td>

                                <td>
                                    ${formatPercent(book.completion)}
                                </td>

                            </tr>

                        `).join("")}

                    </tbody>

                </table>

            </div>
        </div>
    `;
}

function renderAnalytics() {

    const byWords = [...DATA.books]
        .sort((a,b) => b.words.current - a.words.current)
        .slice(0, 12);

    const byProgress = [...DATA.books]
        .sort((a,b) => b.completion - a.completion)
        .slice(0, 12);

    $("#content").innerHTML = `

        <div class="page-head">
            <div>
                <div class="eyebrow">Portfolio Intelligence</div>
                <h1>Analytics.</h1>
                <p>
                    Quantitative view of writing volume,
                    completion and category performance.
                </p>
            </div>
        </div>

        <div class="chart-grid">

            <div class="panel">

                <div class="panel-header">
                    <h2>Books by Word Volume</h2>
                    <span>Top 12</span>
                </div>

                <div class="panel-body">

                    <div class="bar-chart">

                        ${byWords.map(book => {

                            const max =
                                byWords[0]?.words.current || 1;

                            return `

                                <div class="chart-row">

                                    <div class="chart-label">
                                        ${escapeHTML(book.title)}
                                    </div>

                                    <div>
                                        ${progressBar(
                                            book.words.current / max
                                        )}
                                    </div>

                                    <div class="chart-value">
                                        ${formatNumber(book.words.current)}
                                    </div>

                                </div>
                            `;

                        }).join("")}

                    </div>

                </div>
            </div>

            <div class="panel">

                <div class="panel-header">
                    <h2>Book Completion</h2>
                    <span>Highest progress</span>
                </div>

                <div class="panel-body">

                    <div class="bar-chart">

                        ${byProgress.map(book => `

                            <div class="chart-row">

                                <div class="chart-label">
                                    ${escapeHTML(book.title)}
                                </div>

                                <div>
                                    ${progressBar(book.completion)}
                                </div>

                                <div class="chart-value">
                                    ${formatPercent(book.completion)}
                                </div>

                            </div>

                        `).join("")}

                    </div>

                </div>
            </div>

        </div>

        <div style="height:16px"></div>

        <div class="panel">

            <div class="panel-header">
                <h2>Category Analytics</h2>
                <span>Portfolio-wide comparison</span>
            </div>

            <div class="table-wrap">

                <table class="data-table">

                    <thead>
                        <tr>
                            <th>Category</th>
                            <th>Books</th>
                            <th>Chapters</th>
                            <th>Completed</th>
                            <th>Words</th>
                            <th>Target Words</th>
                            <th>Completion</th>
                        </tr>
                    </thead>

                    <tbody>

                        ${DATA.categories.map(category => `

                            <tr>

                                <td>
                                    <span
                                        class="category-link"
                                        onclick="openCategory('${encodeURIComponent(category.name)}')"
                                    >
                                        ${escapeHTML(category.name)}
                                    </span>
                                </td>

                                <td>${category.books}</td>
                                <td>${category.chapters}</td>
                                <td>${category.completed_chapters}</td>
                                <td>${formatNumber(category.words)}</td>
                                <td>${formatNumber(category.target_words)}</td>
                                <td>${formatPercent(category.completion)}</td>

                            </tr>

                        `).join("")}

                    </tbody>

                </table>

            </div>

        </div>
    `;
}

function renderAttention() {

    const items = DATA.attention || [];

    $("#content").innerHTML = `

        <div class="page-head">
            <div>
                <div class="eyebrow">Operational Monitoring</div>
                <h1>Needs attention.</h1>
                <p>
                    Repository-derived issues that may require
                    action before a book can move forward.
                </p>
            </div>
        </div>

        <div class="panel">

            <div class="panel-header">
                <h2>Detected Items</h2>
                <span>${items.length} items</span>
            </div>

            <div class="panel-body">

                ${
                    items.length
                        ? `
                            <div class="attention-list">

                                ${items.map(item => `

                                    <div class="attention-item ${item.severity}">

                                        <strong>
                                            ${escapeHTML(item.book)}
                                        </strong>

                                        <span>
                                            ${escapeHTML(item.message)}
                                        </span>

                                    </div>

                                `).join("")}

                            </div>
                        `
                        : `
                            <div class="empty-state">
                                <strong>No attention items</strong>
                                Your repository currently has no
                                detected operational issues.
                            </div>
                        `
                }

            </div>
        </div>
    `;
}

function openBook(encodedId) {

    const id = decodeURIComponent(encodedId);

    const book = getBook(id);

    if (!book) return;

    const chapters = book.chapters_data || [];

    $("#modalContent").innerHTML = `

        <div class="detail-head">

            <div class="eyebrow">
                ${escapeHTML(book.category)}
            </div>

            <h1>${escapeHTML(book.title)}</h1>

            <p>
                ${escapeHTML(book.id)}
                · ${badge(book.status)}
            </p>

        </div>

        <div class="detail-grid">

            <div class="detail-stat">
                <span>Completion</span>
                <strong>${formatPercent(book.completion)}</strong>
            </div>

            <div class="detail-stat">
                <span>Words</span>
                <strong>${formatNumber(book.words.current)}</strong>
            </div>

            <div class="detail-stat">
                <span>Target Words</span>
                <strong>${formatNumber(book.words.target)}</strong>
            </div>

            <div class="detail-stat">
                <span>Chapters</span>
                <strong>
                    ${book.chapters.completed}/${book.chapters.planned || book.chapters.actual}
                </strong>
            </div>

            <div class="detail-stat">
                <span>Research</span>
                <strong>${escapeHTML(book.pipeline.research)}</strong>
            </div>

            <div class="detail-stat">
                <span>Writing</span>
                <strong>${escapeHTML(book.pipeline.writing)}</strong>
            </div>

            <div class="detail-stat">
                <span>Editing</span>
                <strong>${escapeHTML(book.pipeline.editing)}</strong>
            </div>

            <div class="detail-stat">
                <span>Publishing</span>
                <strong>${escapeHTML(book.pipeline.publishing)}</strong>
            </div>

        </div>

        <div class="detail-section">

            <h2>Book Progress</h2>

            ${progressBar(book.completion)}

        </div>

        <div class="detail-section">

            <h2>Chapters · ${chapters.length}</h2>

            <div class="chapter-list">

                ${
                    chapters.length
                        ? chapters.map(chapter => `

                            <div class="chapter-row">

                                <div class="chapter-number">
                                    CH ${String(chapter.number).padStart(2,"0")}
                                </div>

                                <div>

                                    <div class="chapter-title">
                                        ${escapeHTML(chapter.title)}
                                    </div>

                                    <div style="margin-top:7px">
                                        ${progressBar(
                                            chapter.status === "Completed"
                                                ? 1
                                                : chapter.has_content
                                                    ? .5
                                                    : 0
                                        )}
                                    </div>

                                </div>

                                <div class="chapter-words">
                                    ${formatNumber(chapter.words)} words
                                </div>

                                <div>
                                    ${badge(chapter.status)}
                                </div>

                            </div>

                        `).join("")
                        : `
                            <div class="empty-state">
                                No chapters detected.
                            </div>
                        `
                }

            </div>

        </div>

        <div class="detail-section">

            <h2>Repository</h2>

            <div class="attention-item ${book.repository.found ? "low" : "high"}">

                <strong>
                    ${book.repository.found
                        ? "Repository structure connected"
                        : "Repository structure not found"}
                </strong>

                <span>
                    ${escapeHTML(
                        book.repository.directory ||
                        "No matching directory detected."
                    )}
                </span>

            </div>

        </div>
    `;

    $("#modal").classList.remove("hidden");
}

function openCategory(encodedName) {

    const name = decodeURIComponent(encodedName);

    const books =
        DATA.books.filter(book => book.category === name);

    $("#modalContent").innerHTML = `

        <div class="detail-head">

            <div class="eyebrow">
                Portfolio Category
            </div>

            <h1>${escapeHTML(name)}</h1>

            <p>
                ${books.length} books in this category
            </p>

        </div>

        <div class="detail-section">

            <h2>Books</h2>

            <div class="card-grid">

                ${books.map(bookCard).join("")}

            </div>

        </div>
    `;

    $("#modal").classList.remove("hidden");
}

function closeModal() {
    $("#modal").classList.add("hidden");
}

async function loadData() {

    $("#dataStatus").textContent =
        "Loading repository data...";

    try {

        const response =
            await fetch(
                `./dashboard/data/dashboard-data.json?t=${Date.now()}`,
                {
                    cache: "no-store"
                }
            );

        if (!response.ok) {
            throw new Error(
                `HTTP ${response.status}`
            );
        }

        DATA = await response.json();

        $("#dataStatus").textContent =
            `${DATA.summary.total_books} books connected`;

        $("#attentionCount").textContent =
            DATA.attention?.length || 0;

        render();

    } catch (error) {

        console.error(error);

        $("#dataStatus").textContent =
            "Data load failed";

        $("#content").innerHTML = `

            <div class="empty-state">

                <strong>
                    Dashboard data could not be loaded
                </strong>

                <p>
                    Make sure the Python data generator has been
                    executed and the dashboard is being opened
                    through the local web server.
                </p>

                <p>
                    ${escapeHTML(error.message)}
                </p>

            </div>
        `;
    }
}

document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".nav-item").forEach(item => {

        item.addEventListener(
            "click",
            () => setView(item.dataset.view)
        );

    });

    $("#refreshButton").addEventListener(
        "click",
        loadData
    );

    $("#modalClose").addEventListener(
        "click",
        closeModal
    );

    $("#modalBackdrop").addEventListener(
        "click",
        closeModal
    );

    loadData();

});

window.openBook = openBook;
window.openCategory = openCategory;
window.setView = setView;
