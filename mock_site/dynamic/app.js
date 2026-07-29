const catalogPages = [
  [
    { id: "dyn-001", name: "Browser Automation", category: "books", price: 420 },
    { id: "dyn-002", name: "USB-C Hub", category: "electronics", price: 890 },
  ],
  [
    { id: "dyn-003", name: "Web Testing", category: "books", price: 510 },
    { id: "dyn-004", name: "Desk Lamp", category: "home", price: 650 },
  ],
  [
    { id: "dyn-005", name: "Wireless Keyboard", category: "electronics", price: 1290 },
    { id: "dyn-006", name: "Data Pipelines", category: "books", price: 730 },
  ],
];

const state = { loadedPages: 0, records: [], category: "all" };
const status = document.querySelector("#dynamic-status");
const summary = document.querySelector("#filter-summary");
const tableBody = document.querySelector("#catalog-table tbody");
const loadMore = document.querySelector("#load-more");

function filteredRecords() {
  if (state.category === "all") return state.records;
  return state.records.filter((record) => record.category === state.category);
}

function render() {
  tableBody.replaceChildren();
  for (const record of filteredRecords()) {
    const row = document.createElement("tr");
    for (const value of [record.id, record.name, record.category, record.price]) {
      const cell = document.createElement("td");
      cell.textContent = value;
      row.append(cell);
    }
    tableBody.append(row);
  }
  summary.textContent = `Showing ${filteredRecords().length} of ${state.records.length} loaded records`;
  loadMore.disabled = state.loadedPages >= catalogPages.length;
  status.textContent = `Loaded page ${state.loadedPages} of ${catalogPages.length}`;
}

function loadPage(pageIndex) {
  if (pageIndex >= catalogPages.length) return;
  status.textContent = `Loading page ${pageIndex + 1}...`;
  window.setTimeout(() => {
    state.records.push(...catalogPages[pageIndex]);
    state.loadedPages = pageIndex + 1;
    render();
  }, 50);
}

document.querySelector("#filter-form").addEventListener("submit", (event) => {
  event.preventDefault();
  state.category = document.querySelector("#category-filter").value;
  render();
});

loadMore.addEventListener("click", () => loadPage(state.loadedPages));

document.querySelector("#download-csv").addEventListener("click", () => {
  const header = "id,name,category,price";
  const rows = state.records.map((record) => [record.id, record.name, record.category, record.price].join(","));
  const blob = new Blob([[header, ...rows].join("\n")], { type: "text/csv" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "dynamic-catalog.csv";
  link.click();
  URL.revokeObjectURL(link.href);
});

loadPage(0);
