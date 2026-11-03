// Incident Reporting and Follow-up System — Frontend JavaScript

document.addEventListener('DOMContentLoaded', () => {
  // Auto-dismiss flash messages after 5 seconds
  const flashes = document.querySelectorAll('.flash');
  flashes.forEach((flash) => {
    setTimeout(() => {
      flash.style.opacity = '0';
      flash.style.transition = 'opacity 0.5s ease';
      setTimeout(() => flash.remove(), 500);
    }, 5000);
  });

  // Confirm before deleting
  const deleteForms = document.querySelectorAll('.delete-form');
  deleteForms.forEach((form) => {
    form.addEventListener('submit', (e) => {
      if (!confirm('Are you sure you want to delete this incident?')) {
        e.preventDefault();
      }
    });
  });

  // Style status badges
  const statusMap = {
    Open: 'status-open',
    'In Progress': 'status-in-progress',
    Resolved: 'status-resolved',
    Closed: 'status-closed'
  };

  const statusBadges = document.querySelectorAll('.status-badge');
  statusBadges.forEach((badge) => {
    const status = badge.textContent.trim();
    const cls = statusMap[status];
    if (cls) badge.classList.add(cls);
  });

  // Style category badges
  const categoryMap = {
    Hardware: 'badge-hardware',
    Software: 'badge-software',
    Network: 'badge-network',
    Electrical: 'badge-electrical',
    Facility: 'badge-facility',
    Other: 'badge-other'
  };

  const categoryBadges = document.querySelectorAll('.badge');
  categoryBadges.forEach((badge) => {
    const cat = badge.textContent.trim();
    const cls = categoryMap[cat];
    if (cls) badge.classList.add(cls);
  });

  // Style SLA badges
  const slaMap = {
    'No SLA': 'sla-badge-sla-no-sla',
    Overdue: 'sla-badge-sla-overdue',
    'Due Soon': 'sla-badge-sla-due-soon',
    'On Track': 'sla-badge-sla-on-track'
  };

  const slaBadges = document.querySelectorAll('.sla-badge');
  slaBadges.forEach((badge) => {
    const sla = badge.textContent.trim();
    const cls = slaMap[sla];
    if (cls) badge.classList.add(cls);
  });

  // Highlight overdue rows
  const rows = document.querySelectorAll('.incidents-table tbody tr');
  rows.forEach((row) => {
    const slaCell = row.querySelector('.sla-badge');
    if (slaCell && slaCell.textContent.trim() === 'Overdue') {
      row.style.borderLeft = '4px solid var(--danger)';
    }
  });

  // Dark mode toggle
  const themeToggle = document.getElementById('themeToggle');
  const html = document.documentElement;

  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    html.setAttribute('data-theme', 'dark');
    themeToggle.textContent = '☀️';
  }

  themeToggle.addEventListener('click', () => {
    if (html.getAttribute('data-theme') === 'dark') {
      html.removeAttribute('data-theme');
      localStorage.setItem('theme', 'light');
      themeToggle.textContent = '🌙';
    } else {
      html.setAttribute('data-theme', 'dark');
      localStorage.setItem('theme', 'dark');
      themeToggle.textContent = '☀️';
    }
  });
});