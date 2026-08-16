"""
Product catalog.

Product Generator sử dụng catalog này để sinh product
theo brand và category có sẵn trong database.
"""

PRODUCT_CATALOG = {

    # ======================================================
    # Samsung
    # ======================================================

    "Samsung": {

        "Mobile Phones": [
            "Galaxy S24 Ultra",
            "Galaxy S24+",
            "Galaxy S24",
            "Galaxy S24 FE",
            "Galaxy A56",
            "Galaxy A36",
            "Galaxy A26",
        ],

        "Tablets": [
            "Galaxy Tab S10 Ultra",
            "Galaxy Tab S10+",
            "Galaxy Tab A9",
        ],

        "Accessories": [
            "Galaxy Buds FE",
            "Galaxy Buds3",
            "Galaxy Buds3 Pro",
        ],

        "Watches": [
            "Galaxy Watch Ultra",
            "Galaxy Watch 7",
            "Galaxy Fit 3",
        ],
    },

    # ======================================================
    # Apple
    # ======================================================

    "Apple": {

        "Mobile Phones": [
            "iPhone 16",
            "iPhone 16 Plus",
            "iPhone 16 Pro",
            "iPhone 16 Pro Max",
        ],

        "Laptops": [
            "MacBook Air M4",
            "MacBook Pro 14 M4",
            "MacBook Pro 16 M4",
        ],

        "Tablets": [
            "iPad Air",
            "iPad Pro 11",
            "iPad Pro 13",
        ],

        "Accessories": [
            "AirPods 4",
            "AirPods Pro 2",
            "AirPods Max",
        ],

        "Watches": [
            "Apple Watch Series 10",
            "Apple Watch Ultra 2",
        ],
    },

    # ======================================================
    # Xiaomi
    # ======================================================

    "Xiaomi": {

        "Mobile Phones": [
            "Xiaomi 15",
            "Redmi Note 14",
            "POCO X7",
        ],

        "Tablets": [
            "Xiaomi Pad 7",
            "Xiaomi Pad 7 Pro",
        ],

        "Accessories": [
            "Redmi Buds 6",
            "Xiaomi Buds 5",
        ],

        "Fitness": [
            "Mi Band 9",
            "Xiaomi Watch S4",
        ],
    },

    # ======================================================
    # Oppo
    # ======================================================

    "Oppo": {

        "Mobile Phones": [
            "Oppo Find X8",
            "Oppo Find X8 Pro",
            "Oppo Reno 12",
            "Oppo Reno 12 Pro",
            "Oppo A60",
        ],
    },

    # ======================================================
    # Vivo
    # ======================================================

    "Vivo": {

        "Mobile Phones": [
            "Vivo X200",
            "Vivo X200 Pro",
            "Vivo V40",
            "Vivo V40 Pro",
            "Vivo Y28",
        ],
    },

    # ======================================================
    # Sony
    # ======================================================

    "Sony": {

        "Cameras": [
            "Alpha A7 IV",
            "Alpha A6700",
            "ZV-E10 II",
        ],

        "Accessories": [
            "WH-1000XM5",
            "WF-1000XM5",
            "SRS-XB100",
        ],
    },

    # ======================================================
    # LG
    # ======================================================

    "LG": {

        "Accessories": [
            "LG Tone Free",
            "LG Soundbar S95TR",
            "LG XBOOM Speaker",
        ],
    },

    # ======================================================
    # Dell
    # ======================================================

    "Dell": {

        "Laptops": [
            "Inspiron 15",
            "XPS 13",
            "XPS 15",
            "Latitude 7440",
        ],
    },

    # ======================================================
    # HP
    # ======================================================

    "HP": {

        "Laptops": [
            "Pavilion 15",
            "Victus 15",
            "Spectre x360",
        ],
    },

    # ======================================================
    # Lenovo
    # ======================================================

    "Lenovo": {

        "Laptops": [
            "ThinkPad X1 Carbon",
            "ThinkBook 14",
            "IdeaPad Slim 5",
        ],
    },

    # ======================================================
    # Asus
    # ======================================================

    "Asus": {

        "Laptops": [
            "ROG Zephyrus G16",
            "Vivobook 15",
            "Zenbook 14",
        ],
    },

    # ======================================================
    # Acer
    # ======================================================

    "Acer": {

        "Laptops": [
            "Nitro V 15",
            "Predator Helios Neo",
            "Aspire 5",
        ],
    },

    # ======================================================
    # MSI
    # ======================================================

    "MSI": {

        "Laptops": [
            "MSI Raider GE78",
            "MSI Stealth 16",
            "MSI Katana 15",
            "MSI Cyborg 15",
        ],
    },

    # ======================================================
    # Canon
    # ======================================================

    "Canon": {

        "Cameras": [
            "EOS R8",
            "EOS R10",
            "EOS R6 Mark II",
        ],

        "Accessories": [
            "RF 50mm F1.8",
            "RF 24-105mm F4",
            "RF 70-200mm F2.8",
        ],
    },

    # ======================================================
    # Nikon
    # ======================================================

    "Nikon": {

        "Cameras": [
            "Nikon Z5",
            "Nikon Z6 III",
            "Nikon Z8",
            "Nikon Zf",
        ],
    },

    # ======================================================
    # Nike
    # ======================================================

    "Nike": {

        "Men Clothing": [
            "Nike Dri-FIT T-Shirt",
            "Nike Sportswear Hoodie",
            "Nike Academy Jacket",
        ],

        "Women Clothing": [
            "Nike One Top",
            "Nike Sportswear Leggings",
            "Nike Yoga Jacket",
        ],

        "Shoes": [
            "Air Max 270",
            "Air Force 1",
            "Air Zoom Pegasus",
            "Dunk Low",
        ],

        "Bags": [
            "Nike Brasilia Backpack",
            "Nike Heritage Backpack",
        ],

        "Fitness": [
            "Nike Training Mat",
            "Nike Resistance Band",
        ],

        "Outdoor": [
            "Nike Trail Jacket",
            "Nike ACG Outdoor Shoes",
        ],

        "Running": [
            "Nike Pegasus",
            "Nike Vomero",
            "Nike Structure",
        ],
    },

    # ======================================================
    # Adidas
    # ======================================================

    "Adidas": {

        "Men Clothing": [
            "Adidas Tiro Jersey",
            "Adidas Essentials Hoodie",
            "Adidas Training T-Shirt",
        ],

        "Women Clothing": [
            "Adidas Yoga Top",
            "Adidas Training Leggings",
            "Adidas Sports Bra",
        ],

        "Shoes": [
            "Ultraboost Light",
            "Adidas Superstar",
            "Adidas Stan Smith",
            "Adidas Samba",
        ],

        "Bags": [
            "Adidas Classic Backpack",
            "Adidas Stadium Bag",
        ],

        "Fitness": [
            "Adidas Training Mat",
            "Adidas Resistance Band",
        ],

        "Outdoor": [
            "Adidas Terrex Jacket",
            "Adidas Terrex Shoes",
        ],

        "Running": [
            "Adidas Adizero",
            "Adidas Supernova",
            "Adidas Ultraboost",
        ],
    },

    # ======================================================
    # Puma
    # ======================================================

    "Puma": {

        "Men Clothing": [
            "Puma Essentials T-Shirt",
            "Puma Training Hoodie",
            "Puma Team Jersey",
        ],

        "Women Clothing": [
            "Puma Training Top",
            "Puma Active Leggings",
            "Puma Sports Bra",
        ],

        "Shoes": [
            "Puma Suede Classic",
            "Puma RS-X",
            "Puma Future Rider",
        ],

        "Fitness": [
            "Puma Training Gloves",
            "Puma Training Mat",
        ],

        "Running": [
            "Puma Velocity Nitro",
            "Puma Deviate Nitro",
        ],
    },

    # ======================================================
    # Converse
    # ======================================================

    "Converse": {

        "Men Clothing": [
            "Converse Graphic T-Shirt",
            "Converse Hoodie",
        ],

        "Women Clothing": [
            "Converse Women's T-Shirt",
            "Converse Women's Hoodie",
        ],

        "Shoes": [
            "Chuck Taylor All Star",
            "Chuck 70",
            "Run Star Hike",
        ],
    },
}