document.addEventListener('DOMContentLoaded', () => {
    console.log('StyleSync UI Engine Booting...');
    
    // Safe DOM Element Selector helper function
    const getEl = (id) => {
        const el = document.getElementById(id);
        if (!el) console.warn(`Warning: Element with ID "${id}" was not found in index.html`);
        return el;
    };

    const productSelect = getEl('product-select');
    const syncBtn = getEl('sync-btn');
    const loadingSpinner = getEl('loading-spinner');
    const recGrid = getEl('recommendations-grid');
    
    const selectedProfile = getEl('selected-profile');
    const profileBrand = getEl('profile-brand');
    const profileColor = getEl('profile-color');
    const profilePrice = getEl('profile-price');
    
    const itemDetailsSection = getEl('item-details-section');
    const detailsCategory = getEl('details-category');
    const detailsShade = getEl('details-shade');
    const detailsDescription = getEl('details-description');

    let localCatalog = [];

    // 1. Fetch products list from Flask API backend
    if (productSelect) {
        fetch('/api/products')
            .then(response => response.json())
            .then(data => {
                localCatalog = data;
                productSelect.innerHTML = '<option value="" disabled selected>-- Choose an item --</option>';
                data.forEach(product => {
                    const option = document.createElement('option');
                    option.value = product.productId;
                    option.textContent = `${product.productName} (${product.colorName})`;
                    productSelect.appendChild(option);
                });
            })
            .catch(err => console.error('Error fetching catalog:', err));
    }

    // 2. Watch for selection dropdown changes
    if (productSelect) {
        productSelect.addEventListener('change', (e) => {
            const selectedId = e.target.value;
            const matchedItem = localCatalog.find(item => String(item.productId) === String(selectedId));
            if (matchedItem) {
                if (profileBrand) profileBrand.textContent = matchedItem.brandName || 'H&M';
                if (profileColor) profileColor.textContent = matchedItem.colorName;
                if (profilePrice) profilePrice.textContent = matchedItem.price ? `$${matchedItem.price}` : '$29.99';
                if (selectedProfile) selectedProfile.classList.remove('hidden');
            }
        });
    }

    // 3. Handle click event on the recommendation action button
    if (syncBtn) {
        syncBtn.addEventListener('click', () => {
            console.log('Sync button clicked, executing pipeline...');
            const selectedProductId = productSelect ? productSelect.value : null;
            if (!selectedProductId) {
                alert('Please select a clothing item from the dropdown first.');
                return;
            }

            if (recGrid) recGrid.innerHTML = '';
            if (loadingSpinner) loadingSpinner.classList.remove('hidden');
            if (itemDetailsSection) itemDetailsSection.classList.add('hidden');

            fetch(`/api/recommend?id=${selectedProductId}`)
                .then(response => response.json())
                .then(data => {
                    if (loadingSpinner) loadingSpinner.classList.add('hidden');
                    if (data.error) {
                        alert(`Error: ${data.error}`);
                        return;
                    }

                    if (data.length > 0 && itemDetailsSection) {
                        const firstMatch = data[0];
                        if (detailsCategory) detailsCategory.textContent = firstMatch.brandName || 'Fashion Apparel';
                        if (detailsShade) detailsShade.textContent = firstMatch.colorName;
                        
                        let rawDetails = firstMatch.details || 'No detailed description available.';
                        if (rawDetails.length > 150) {
                            rawDetails = rawDetails.substring(0, 147) + '...';
                        }
                        if (detailsDescription) detailsDescription.textContent = rawDetails;
                        itemDetailsSection.classList.remove('hidden');
                    }

                    if (recGrid) {
                        data.forEach(item => {
                        const card = document.createElement('div');
                        // Ensure this class name matches your exact CSS stylesheet selector
                        card.className = 'rec-card'; 
        
                        card.innerHTML = `
                            <span class="match-tag">Match</span>
                            <h4 style="margin: 10px 0 5px 0; color: #fff;">${item.productName || 'Fashion Item'}</h4>
                            <p style="margin: 2px 0; color: #ccc;"><strong>Color:</strong> ${item.colorName || 'Multi'}</p>
                            <p style="margin: 2px 0; color: #ccc;"><strong>Brand:</strong> ${item.brandName || 'H&M'}</p>
                            <span class="price" style="display: block; margin-top: 10px; color: #ff4a5a; font-weight: bold;">$${item.price || '19.99'}</span>
                        `;
                        recGrid.appendChild(card);
                        });
                    }
                })
                .catch(err => {
                    if (loadingSpinner) loadingSpinner.classList.add('hidden');
                    console.error('Error syncing matches:', err);
                });
        });
    }
});