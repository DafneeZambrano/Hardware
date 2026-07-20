import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix parseInt for data-id in renderPDP
# Line 1276: const clickedItemId = parseInt(e.currentTarget.getAttribute('data-id'));
# Line 1279: renderPDP(clickedItemId);
# Wait, renderPDP takes productId. If productId is a string, it works.
# But products.find(p => p.id === productId) uses ===.
# So if productId is a string and p.id is a number, it will fail.
# Let's change `p.id === productId` to `String(p.id) === String(productId)` in renderPDP.

content = content.replace(
    "const product = products.find(p => p.id === productId);",
    "const product = products.find(p => String(p.id) === String(productId));"
)

content = content.replace(
    "const clickedItemId = parseInt(e.currentTarget.getAttribute('data-id'));",
    "const clickedItemId = e.currentTarget.getAttribute('data-id');"
)

content = content.replace(
    "const itemProd = products.find(p => p.id === parseInt(row.getAttribute('data-id')));",
    "const itemProd = products.find(p => String(p.id) === String(row.getAttribute('data-id')));"
)

# Wait, there's another one:
# let bomItems = products.filter(p => p.partOfKit === kitId || (kitId === 31 && ...));
# If kitId is a string, `kitId === 31` is false, which is correct.
# But `p.partOfKit === kitId` uses `===`. If `partOfKit` is a number and `kitId` is a string, it fails.
# Let's change `showBomModal` to use `String(p.partOfKit) === String(kitId)`
content = content.replace(
    "let bomItems = products.filter(p => p.partOfKit === kitId || (kitId === 31 && (p.id === 10 || p.id === 17 || p.id === 20)));",
    "let bomItems = products.filter(p => String(p.partOfKit) === String(kitId) || (String(kitId) === '31' && (p.id === 10 || p.id === 17 || p.id === 20)));"
)

# And in renderPDP:
# let bomItems = products.filter(p => p.partOfKit === product.id || (product.id === 31 && ...));
content = content.replace(
    "let bomItems = products.filter(p => p.partOfKit === product.id || (product.id === 31 && (p.id === 10 || p.id === 17 || p.id === 20)));",
    "let bomItems = products.filter(p => String(p.partOfKit) === String(product.id) || (String(product.id) === '31' && (p.id === 10 || p.id === 17 || p.id === 20)));"
)

# Also check addToCart. It might use `product.id`.
# cart.push({ id: product.id, ... })
# That's fine.

with open('index.html', 'w') as f:
    f.write(content)
