function toggleAdvancedSearch() {
    const advancedSearch = document.getElementById('advanced-search');
    const toggleButton = document.querySelector('.btn-toggle');
    if (advancedSearch.style.display === 'none' || advancedSearch.style.display === '') {
        advancedSearch.style.display = 'block';
        toggleButton.classList.add('active');
    } else {
        advancedSearch.style.display = 'none';
        toggleButton.classList.remove('active');
    }
}