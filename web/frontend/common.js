const API = "http://127.0.0.1:5000/api";

async function apiFetch(path, options = {}) {
  const res = await fetch(API + path, options);
  const data = await res.json();
  if (!res.ok) throw data;
  return data;
}

function statusBadge(status) {
  const normalized = (status || "").toLowerCase();
  if (normalized === "success") {
    return '<span class="badge badge-success">Success</span>';
  }
  if (normalized === "failed" || normalized === "error") {
    return '<span class="badge badge-failed">Failed</span>';
  }
  if (normalized === "running") {
    return '<span class="badge badge-running">Running</span>';
  }
  return '<span class="badge badge-unknown">Unknown</span>';
}

function getQueryParam(name) {
  const params = new URLSearchParams(window.location.search);
  return params.get(name);
}

function markActiveNav() {
  const path = window.location.pathname || "";
  const current = path.split("/").pop() || "experiments.html";

  document
    .querySelectorAll(".nav-link[data-page]")
    .forEach((el) => {
      const page = el.getAttribute("data-page");
      if (page === current) {
        el.classList.add("active");
      } else {
        el.classList.remove("active");
      }
    });
}

document.addEventListener("DOMContentLoaded", () => {
  markActiveNav();
});
