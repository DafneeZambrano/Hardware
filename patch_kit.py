import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update products array
new_products = """            { id: "kit-geo-survey-01", name: "Trimble Land Surveying & Mapping Kit", industry: "Geospatial", system: "Survey & Optical Systems", type: "GNSS Receivers & Smart Antennas", brand: "Trimble", machineCompatibility: "None (Pole/Tripod Mounted)", description: "Complete high-precision GNSS field rover system for land surveying, mapping, and topographic data collection.", isKit: true, keywords: ["land surveying", "mapping", "rover system"], price: 16500, estimatedDelivery: "Less than 10 days", inventoryStatus: "In Stock", image: "https://images.unsplash.com/photo-1581092580497-e0d23cbdf1dc?auto=format&fit=crop&w=600&q=80" },
            { id: "geo-r12i", name: "Trimble R12i GNSS Receiver", industry: "Geospatial", system: "Survey & Optical Systems", type: "GNSS Receivers & Smart Antennas", brand: "Trimble", machineCompatibility: "None (Pole/Tripod Mounted)", description: "Sub-centimeter RTK with Tilt Compensation", partOfKit: "kit-geo-survey-01", kitDetails: "GNSS Receiver", price: 12500, estimatedDelivery: "Less than 10 days", inventoryStatus: "In Stock" },
            { id: "geo-tsc5", name: "Trimble TSC5 Controller", industry: "Geospatial", system: "Survey & Optical Systems", type: "Controllers & Data Collectors", brand: "Trimble", machineCompatibility: "None (Pole/Tripod Mounted)", description: "5-inch Rugged Field Screen with Android OS", partOfKit: "kit-geo-survey-01", kitDetails: "Controller", price: 3200, estimatedDelivery: "Less than 10 days", inventoryStatus: "In Stock" },
            { id: "geo-pole", name: "Carbon Fiber Rover Pole & Mount Bracket", industry: "Geospatial", system: "Survey & Optical Systems", type: "Accessories (Power, Brackets, Cases)", brand: "Trimble", machineCompatibility: "None (Pole/Tripod Mounted)", description: "2-meter telescoping with quick-release bracket", partOfKit: "kit-geo-survey-01", kitDetails: "Rover Pole", price: 450, estimatedDelivery: "Less than 10 days", inventoryStatus: "In Stock" },
            { id: "geo-batt", name: "Dual Smart Battery & Charger Kit", industry: "Geospatial", system: "Survey & Optical Systems", type: "Accessories (Power, Brackets, Cases)", brand: "Trimble", machineCompatibility: "None (Pole/Tripod Mounted)", description: "Li-Ion rechargeable with dual-bay charger", partOfKit: "kit-geo-survey-01", kitDetails: "Battery & Charger", price: 350, estimatedDelivery: "Less than 10 days", inventoryStatus: "In Stock" },
"""

content = content.replace(
    '        const products = [\n',
    '        const products = [\n' + new_products
)

# 2. Update getProductSvg to use image if available
old_svg_func = """        function getProductSvg(product) {
            let path = '';
            switch(product.type) {"""
new_svg_func = """        function getProductSvg(product) {
            if (product.image) {
                return `<img src="${product.image}" alt="${product.name || 'Hardware Asset'}" style="width: 100%; height: 100%; object-fit: contain; background-color: #f3f4f6; border-radius: 4px; display: block;" />`;
            }
            let path = '';
            switch(product.type) {"""

content = content.replace(old_svg_func, new_svg_func)

# 3. Update showBomModal
old_bom = "let bomItems = products.filter(p => p.partOfKit === kitId || p.id === 10 || p.id === 17 || p.id === 20);"
new_bom = "let bomItems = products.filter(p => p.partOfKit === kitId || (kitId === 31 && (p.id === 10 || p.id === 17 || p.id === 20)));"
content = content.replace(old_bom, new_bom)

with open('index.html', 'w') as f:
    f.write(content)
