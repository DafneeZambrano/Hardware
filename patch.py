import re

with open('hardware.html', 'r') as f:
    content = f.read()

# Add order-details-view HTML
order_details_html = """
        <div id="order-details-view" style="display: none; padding-bottom: 4rem;">
            <!-- Top-left layout -->
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 2rem;">
                <div>
                    <a href="#" id="order-details-back-to-catalog" style="text-decoration: underline; color: #4b5563; font-weight: bold; cursor: pointer; display: inline-block; margin-bottom: 1rem;">&larr; Back to Hardware Catalog</a>
                    <h1 style="font-size: 2.5rem; margin: 0 0 0.5rem 0; font-weight: bold;">Order Details</h1>
                    <p style="color: #4b5563; font-size: 1.1rem; margin: 0;" id="order-details-metadata">Order placed: [Current Date] | Order #[OrderNum]</p>
                </div>
                <div>
                    <button class="product-btn" style="background-color: transparent; color: #111827; border: 2px solid #111827; padding: 0.5rem 1.5rem;">View invoice</button>
                </div>
            </div>

            <!-- 3-Column Information Row -->
            <div style="display: flex; flex-wrap: wrap; border: 2px solid var(--border-color); background: #fff; margin-bottom: 2rem;">
                <!-- Column 1: Ship to -->
                <div style="flex: 1; min-width: 250px; padding: 1.5rem; border-right: 2px solid var(--border-color); box-sizing: border-box;">
                    <h3 style="margin-top: 0; margin-bottom: 1rem; font-size: 1.1rem;">Ship to</h3>
                    <div style="color: #4b5563; line-height: 1.5; margin-bottom: 1rem;">
                        California warehouse, 1234 Construction Ave, San Francisco, CA 97201
                    </div>
                    <a href="#" style="color: #4b5563; text-decoration: underline; font-weight: bold;">Change shipping address</a>
                </div>
                <!-- Column 2: Payment method -->
                <div style="flex: 1; min-width: 250px; padding: 1.5rem; border-right: 2px solid var(--border-color); box-sizing: border-box;">
                    <h3 style="margin-top: 0; margin-bottom: 1rem; font-size: 1.1rem;">Payment method</h3>
                    <div style="color: #4b5563; line-height: 1.5; margin-bottom: 1rem;">
                        <strong>Payment Method:</strong> Corporate Account Invoice Reference<br>
                        <strong>Billing Account:</strong> Trimble Civil-Corp #98344<br>
                        <strong>Payment Terms:</strong> Net 30 Days
                    </div>
                    <a href="#" style="color: #4b5563; text-decoration: underline; font-weight: bold;">View related transactions</a>
                </div>
                <!-- Column 3: Order Summary -->
                <div style="flex: 1; min-width: 250px; padding: 1.5rem; box-sizing: border-box;">
                    <h3 style="margin-top: 0; margin-bottom: 1rem; font-size: 1.1rem;">Order Summary</h3>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; color: #4b5563;">
                        <span>Item(s) Subtotal:</span>
                        <span id="order-details-subtotal">$0.00</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; color: #4b5563;">
                        <span>Shipping & Handling:</span>
                        <span>$0.00</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; color: #4b5563;">
                        <span>Total before tax:</span>
                        <span id="order-details-pretax">$0.00</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 1rem; color: #4b5563;">
                        <span>Estimated tax to be collected:</span>
                        <span id="order-details-tax">$0.00</span>
                    </div>
                    <div style="border-top: 1px solid var(--border-color); margin-bottom: 1rem;"></div>
                    <div style="display: flex; justify-content: space-between; font-weight: bold; font-size: 1.1rem;">
                        <span>Grand Total:</span>
                        <span id="order-details-total">$0.00</span>
                    </div>
                </div>
            </div>

            <!-- Shipment & Item List Cards Container -->
            <div id="order-details-shipments-container" style="display: flex; flex-direction: column; gap: 2rem;">
                <!-- dynamic shipments go here -->
            </div>
        </div>
"""

# Find where to insert order-details-view
confirmation_end = content.find('        <!-- Dynamic Address Modal -->')
if confirmation_end != -1:
    content = content[:confirmation_end] + order_details_html + content[confirmation_end:]

# Update View or manage order button
content = content.replace(
    '<button class="product-btn" style="background-color: #f9f9f9; color: var(--text-color); border: 2px solid var(--border-color); padding: 0.75rem 2rem; font-weight: bold;">View or manage order</button>',
    '<button id="view-manage-order-btn" class="product-btn" style="background-color: #f9f9f9; color: var(--text-color); border: 2px solid var(--border-color); padding: 0.75rem 2rem; font-weight: bold;">View or manage order</button>'
)

# Add lastOrder variable
content = content.replace('        let cart = [];', '        let cart = [];\n        let lastOrder = null;')

# Replace placeOrderBtn logic
place_order_start = content.find('const placeOrderBtn = document.getElementById(\'place-order-btn\');')
place_order_end = content.find('const confirmationBackBtn = document.getElementById(\'confirmation-back-to-catalog\');')

new_place_order_logic = """const placeOrderBtn = document.getElementById('place-order-btn');
        if (placeOrderBtn) {
            placeOrderBtn.addEventListener('click', () => {
                const checkoutItems = cart.filter(item => item.activeForCheckout);
                const deliveryTimes = checkoutItems.map(item => {
                    const product = products.find(p => p.id === item.id);
                    return product ? product.estimatedDelivery : "Less than 10 days";
                });
                
                const uniqueTimes = [...new Set(deliveryTimes)];
                let displayDelivery = "";
                
                if (uniqueTimes.length === 1) {
                    displayDelivery = uniqueTimes[0];
                } else {
                    displayDelivery = `Multiple delivery time frames apply.<br><span style='font-size: 13px; color: #6b7280; font-weight: normal;'>Please view or manage order</span>`;
                }
                
                document.getElementById('dynamic-delivery-time').innerHTML = `<strong>${displayDelivery}</strong>`;

                const orderNum = Math.floor(100000 + Math.random() * 900000);
                document.getElementById('dynamic-order-number').textContent = `Order #TRM-2026-${orderNum}`;
                
                // Calculate totals for lastOrder
                let orderSubtotal = 0;
                const enrichedItems = checkoutItems.map(item => {
                    const product = products.find(p => p.id === item.id);
                    if (product) {
                        orderSubtotal += product.price * item.quantity;
                    }
                    return { ...item, product };
                });
                const orderTax = orderSubtotal * 0.0825;
                const orderTotal = orderSubtotal + orderTax;

                const options = { month: 'long', day: 'numeric', year: 'numeric' };
                lastOrder = {
                    orderNum: `TRM-2026-${orderNum}`,
                    items: enrichedItems,
                    subtotal: orderSubtotal,
                    tax: orderTax,
                    total: orderTotal,
                    date: new Date().toLocaleDateString('en-US', options)
                };

                cart = [];
                updateNavbarCartBadge();
                document.getElementById('checkout-view').style.display = 'none';
                document.getElementById('mini-cart-sidebar').style.display = 'none';
                document.getElementById('confirmation-view').style.display = 'block';
                window.scrollTo(0, 0);
            });
        }

        """

content = content[:place_order_start] + new_place_order_logic + content[place_order_end:]

# Inject javascript for Order details interaction
script_injection = """
        const viewManageOrderBtn = document.getElementById('view-manage-order-btn');
        if (viewManageOrderBtn) {
            viewManageOrderBtn.addEventListener('click', () => {
                document.getElementById('confirmation-view').style.display = 'none';
                document.getElementById('order-details-view').style.display = 'block';
                window.scrollTo(0, 0);
                
                if (lastOrder) {
                    document.getElementById('order-details-metadata').textContent = `Order placed: ${lastOrder.date} | Order #${lastOrder.orderNum}`;
                    
                    const formatPrice = (price) => '$' + price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
                    
                    document.getElementById('order-details-subtotal').textContent = formatPrice(lastOrder.subtotal);
                    document.getElementById('order-details-pretax').textContent = formatPrice(lastOrder.subtotal);
                    document.getElementById('order-details-tax').textContent = formatPrice(lastOrder.tax);
                    document.getElementById('order-details-total').textContent = formatPrice(lastOrder.total);
                    
                    // Group items by shipment timeline
                    const shipments = {};
                    lastOrder.items.forEach(item => {
                        const delivery = item.product ? item.product.estimatedDelivery : "Less than 10 days";
                        if (!shipments[delivery]) shipments[delivery] = [];
                        shipments[delivery].push(item);
                    });
                    
                    const container = document.getElementById('order-details-shipments-container');
                    container.innerHTML = '';
                    
                    for (const [deliveryTime, items] in Object.entries(shipments)) {
                        // We will fix the loop below
                    }
                    
                    Object.entries(shipments).forEach(([deliveryTime, items]) => {
                        const shipmentDiv = document.createElement('div');
                        shipmentDiv.style.border = '2px solid var(--border-color)';
                        shipmentDiv.style.background = '#fff';
                        shipmentDiv.style.padding = '1.5rem';
                        
                        // Header
                        const header = document.createElement('h2');
                        header.style.marginTop = '0';
                        header.style.marginBottom = '1.5rem';
                        header.style.fontSize = '1.5rem';
                        header.textContent = `Arriving: ${deliveryTime}`;
                        shipmentDiv.appendChild(header);
                        
                        const shipmentContent = document.createElement('div');
                        shipmentContent.style.display = 'flex';
                        shipmentContent.style.justifyContent = 'space-between';
                        shipmentContent.style.gap = '2rem';
                        shipmentContent.style.flexWrap = 'wrap';
                        
                        // Left-Side Items List
                        const itemsList = document.createElement('div');
                        itemsList.style.flex = '1';
                        itemsList.style.minWidth = '300px';
                        itemsList.style.display = 'flex';
                        itemsList.style.flexDirection = 'column';
                        itemsList.style.gap = '1.5rem';
                        
                        items.forEach(item => {
                            const p = item.product || { name: 'Unknown Item', price: 0 };
                            
                            const itemRow = document.createElement('div');
                            itemRow.style.display = 'flex';
                            itemRow.style.gap = '1.5rem';
                            itemRow.style.alignItems = 'flex-start';
                            
                            // SVG Icon
                            const svgContainer = document.createElement('div');
                            svgContainer.style.width = '80px';
                            svgContainer.style.height = '80px';
                            svgContainer.style.flexShrink = '0';
                            svgContainer.innerHTML = `
                                <svg width="100%" height="100%" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="background-color: #F3F4F6; border: 1px solid #E5E7EB;">
                                    <path d="M50 25 C30 25, 15 35, 15 50 C15 65, 30 75, 50 75 C70 75, 85 65, 85 50 C85 35, 70 25, 50 25 Z" fill="#9CA3AF"/>
                                    <text x="50" y="55" font-family="sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">ITEM</text>
                                </svg>
                            `;
                            
                            const infoDiv = document.createElement('div');
                            infoDiv.style.flex = '1';
                            infoDiv.innerHTML = `
                                <div style="font-weight: bold; color: #111827; margin-bottom: 0.25rem;">${p.name}</div>
                                <div style="color: #4b5563; margin-bottom: 0.25rem; font-weight: bold;">${formatPrice(p.price)}</div>
                                <div style="color: #6b7280; margin-bottom: 1rem;">Qty: ${item.quantity}</div>
                                <button class="product-btn" style="background-color: transparent; color: #111827; border: 2px solid var(--border-color); padding: 0.5rem 1.5rem; font-weight: bold;">Buy it again</button>
                            `;
                            
                            itemRow.appendChild(svgContainer);
                            itemRow.appendChild(infoDiv);
                            itemsList.appendChild(itemRow);
                        });
                        
                        // Right-Side Shipment Button Stack
                        const actionStack = document.createElement('div');
                        actionStack.style.display = 'flex';
                        actionStack.style.flexDirection = 'column';
                        actionStack.style.gap = '1rem';
                        actionStack.style.minWidth = '250px';
                        actionStack.innerHTML = `
                            <button class="product-btn" style="width: 100%; background-color: #111827; color: #fff; border: 2px solid #111827; padding: 0.75rem;">Track package</button>
                            <button class="product-btn" style="width: 100%; background-color: transparent; color: #111827; border: 2px solid var(--border-color); padding: 0.75rem;">Report a problem with order</button>
                        `;
                        
                        shipmentContent.appendChild(itemsList);
                        shipmentContent.appendChild(actionStack);
                        shipmentDiv.appendChild(shipmentContent);
                        container.appendChild(shipmentDiv);
                    });
                }
            });
        }
        
        const orderDetailsBackBtn = document.getElementById('order-details-back-to-catalog');
        if (orderDetailsBackBtn) {
            orderDetailsBackBtn.addEventListener('click', (e) => {
                e.preventDefault();
                document.getElementById('order-details-view').style.display = 'none';
                document.getElementById('catalog-view').style.display = 'block';
                window.scrollTo(0, 0);
            });
        }
"""

script_end = content.rfind('</script>')
content = content[:script_end] + script_injection + content[script_end:]

with open('hardware.html', 'w') as f:
    f.write(content)
