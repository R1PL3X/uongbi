/* ===================== Uong Bi GO - API helper dung chung ===================== */
const API_BASE = "https://j3390qx4-8000.asse.devtunnels.ms/api";

const Auth = {
  getToken() {
    try { return localStorage.getItem("ubg_token"); } catch (e) { return null; }
  },
  getUser() {
    try { return JSON.parse(localStorage.getItem("ubg_user") || "null"); } catch (e) { return null; }
  },
  setSession(token, user) {
    try {
      localStorage.setItem("ubg_token", token);
      localStorage.setItem("ubg_user", JSON.stringify(user));
    } catch (e) { /* trinh duyet chan luu tru - bo qua, session se khong ton tai sau reload */ }
  },
  clear() {
    try {
      localStorage.removeItem("ubg_token");
      localStorage.removeItem("ubg_user");
    } catch (e) { /* noop */ }
  },
  isLoggedIn() { return !!this.getToken(); },
  requireRole(allowedRoles) {
    const user = this.getUser();
    if (!this.isLoggedIn() || !user) {
      window.location.href = "/index.html";
      return null;
    }
    if (allowedRoles && !allowedRoles.includes(user.vaiTro)) {
      alert("Tai khoan cua ban khong co quyen truy cap trang nay.");
      redirectByRole(user.vaiTro);
      return null;
    }
    return user;
  },
};

function redirectByRole(vaiTro) {
  const map = { ROLE_BUYER: "/menu.html", ROLE_STAFF: "/kds.html", ROLE_ADMIN: "/admin/dashboard.html" };
  window.location.href = map[vaiTro] || "/index.html";
}

/**
 * Goi API co dinh kem JWT token (neu co). Neu 401 -> tu dong dang xuat va quay ve trang login.
 */
async function apiFetch(path, options = {}) {
  const headers = Object.assign({}, options.headers || {});
  if (!(options.body instanceof FormData) && options.body) {
    headers["Content-Type"] = "application/json";
  }
  const token = Auth.getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  let response;
  try {
    response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  } catch (networkError) {
    // Risk #5 - Mat ket noi mang: khong de UI bi crash, nem loi co cau truc de noi goi xu ly hien thong bao.
    throw { networkError: true, message: "Khong the ket noi toi may chu. Vui long kiem tra ket noi mang." };
  }

  if (response.status === 401) {
    Auth.clear();
    window.location.href = "/index.html";
    throw { message: "Phien dang nhap da het han, vui long dang nhap lai." };
  }

  let data = null;
  const text = await response.text();
  if (text) {
    try { data = JSON.parse(text); } catch (e) { data = text; }
  }

  if (!response.ok) {
    const message = (data && (data.detail || data.message)) || `Loi ${response.status}`;
    throw { status: response.status, message, data };
  }
  return data;
}

function formatCurrency(value) {
  return new Intl.NumberFormat("vi-VN").format(Math.round(value)) + "đ";
}

function formatDateTime(isoString) {
  try {
    const d = new Date(isoString);
    return d.toLocaleString("vi-VN", { hour: "2-digit", minute: "2-digit", day: "2-digit", month: "2-digit", year: "numeric" });
  } catch (e) { return isoString; }
}

const STATUS_LABEL = {
  CHO_THANH_TOAN: "Cho thanh toan",
  DA_THANH_TOAN: "Da thanh toan",
  DANG_CHUAN_BI: "Dang chuan bi",
  SAN_SANG_NHAN: "San sang nhan",
  HOAN_THANH: "Hoan thanh",
  DA_HUY: "Da huy",
};

function statusPillHtml(trangThai) {
  const label = STATUS_LABEL[trangThai] || trangThai;
  return `<span class="status-pill status-${trangThai}">${label}</span>`;
}

/* ---------- Risk #5: bao mat ket noi mang, hien banner khi mat mang ---------- */
function initOfflineBanner() {
  const banner = document.createElement("div");
  banner.className = "offline-banner hidden";
  banner.innerHTML = '<span class="dot"></span><span>Mat ket noi mang - dang cho ket noi lai de dong bo...</span>';
  document.body.appendChild(banner);

  function updateStatus() {
    if (navigator.onLine) {
      banner.classList.add("hidden");
    } else {
      banner.classList.remove("hidden");
    }
  }
  window.addEventListener("online", () => {
    updateStatus();
    // Khi co mang tro lai, phat 1 su kien tuy chinh de trang tu dong dong bo (sync) du lieu bi lo
    window.dispatchEvent(new CustomEvent("ubg:reconnected"));
  });
  window.addEventListener("offline", updateStatus);
  updateStatus();
}

document.addEventListener("DOMContentLoaded", initOfflineBanner);
