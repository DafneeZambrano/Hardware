with open('hardware.html', 'r') as f:
    content = f.read()

bad_str = """                    for (const [deliveryTime, items] in Object.entries(shipments)) {
                        // We will fix the loop below
                    }
                    """

content = content.replace(bad_str, "")

with open('hardware.html', 'w') as f:
    f.write(content)
