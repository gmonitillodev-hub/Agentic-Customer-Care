EVAL_DATASET_25 = [
    # FAQ
    {
        "question": "Do I need an account to place an order and what do I gain by creating one?",
        "ground_truth": "No, you can check out as a guest. A free account lets you track orders, save addresses, view order "
                        "history, earn rewards points, and manage returns more easily.",
    },
    {
        "question": "How can a guest track an order?",
        "ground_truth": "Guest orders can be tracked at greenthumb.com/track using the order number and email address.",
    },
    {
        "question": "Is my payment information secure and how is sales tax calculated?",
        "ground_truth": "Yes. All transactions are encrypted with 256-bit SSL, the site is PCI-DSS compliant and never stores full "
                        "credit card numbers. Sales tax is calculated based on the shipping destination, according to state and "
                        "local tax laws.",
    },
    # Policies
    {
        "question": "What is the return window and what conditions must an item meet to be returned?",
        "ground_truth": "The return window is 30 days from the date of delivery. Items must be unused, in original packaging and "
                        "in resalable condition, and proof of purchase (order confirmation email or order number) is required.",
    },
    {
        "question": "Can I return an opened bag of soil or fertilizer?",
        "ground_truth": "No. Only unopened bags of soil, mulch and fertilizer can be returned within 30 days; opened bags are not "
                        "eligible for return.",
    },
    {
        "question": "How long do I have to report a plant damaged in transit and what must I send?",
        "ground_truth": "You must report it within 48 hours of delivery, with clear photographs of the damaged plant and of the "
                        "packaging, by emailing plantcare@greenthumb.com or calling 1-800-555-GROW. You get a free replacement or "
                        "full refund, and you do not need to ship the plant back.",
    },
    {
        "question": "What is the warranty period for hand tools, cutting tools and irrigation equipment?",
        "ground_truth": "Hand tools such as pruners, trowels and rakes have a 5-year warranty, cutting tools such as loppers and "
                        "hedge shears have 3 years, and irrigation equipment such as timers, drip kits and hoses has 1 year.",
    },
    {
        "question": "What are the standard and express shipping costs and delivery times?",
        "ground_truth": "Standard shipping takes 5-7 business days and is free on orders over $50, otherwise $5.99. Express "
                        "shipping takes 1-2 business days and costs $24.99.",
    },
    # Platform errors
    {
        "question": "What is the cause and solution of ERR004?",
        "ground_truth": "ERR004 is a user authentication failure. Ensure the user is entering the correct credentials, offer "
                        "password reset options and check for server-side authentication issues.",
    },
    {
        "question": "A customer cannot ship the order because no delivery option is offered at checkout. Which error is it?",
        "ground_truth": "It is ERR007, shipping method unavailable. Review shipping zones and rates configuration, ensure the "
                        "carrier APIs are reachable and offer alternative shipping options if available.",
    },
    {
        "question": "A user was logged out in the middle of checkout. Which error is this and what should be done?",
        "ground_truth": "It is ERR010, session expired. Notify the user and prompt them to log in again, and extend the session "
                        "timeout settings if appropriate.",
    },
    # Garden info
    {
        "question": "When and where should I plant roses and how far apart?",
        "ground_truth": "Plant roses in early spring after the last frost or in fall (6 weeks before the first frost), in full "
                        "sun with at least 6 hours of direct sunlight, spaced 2-3 feet apart in rich, well-drained, slightly "
                        "acidic soil (pH 6.0-6.5).",
    },
    {
        "question": "What are the options to lower soil pH and how accurate is a home test kit?",
        "ground_truth": "To lower pH you can use elemental sulfur (slow but long-lasting, 1-2 lbs per 100 sq ft), iron sulfate "
                        "(faster but shorter), peat moss or pine needle mulch. Home test kits are accurate to about ±0.5 pH "
                        "units, good for general guidance.",
    },
    {
        "question": "What is the ideal ratio of browns to greens in a compost pile and what should I not compost?",
        "ground_truth": "Aim for about 3 parts browns to 1 part greens by volume. Do not compost meat, fish and bones, dairy, "
                        "cooking oils and grease, pet waste, diseased plants or weeds with seeds, or chemically treated wood or "
                        "plants.",
    },
    {
        "question": "Which organic fertilizer is gentle enough that it cannot burn seedlings?",
        "ground_truth": "Worm castings (1-0-0) give gentle, balanced nutrition, cannot burn plants and are perfect for seedlings "
                        "and containers.",
    },
    {
        "question": "What is a simple homemade all-purpose organic fertilizer blend?",
        "ground_truth": "Mix 4 parts seed meal (alfalfa or soybean), 1 part bone meal and 1 part kelp meal, and apply 4-6 cups "
                        "per 100 square feet of garden bed.",
    },
    {
        "question": "What lawn care tasks should I do in autumn?",
        "ground_truth": "Aerate compacted lawns to improve water and nutrient penetration, overseed bare patches with "
                        "cool-season grass seed and apply a fall fertilizer to strengthen roots before winter.",
    },
    {
        "question": "How much does mulch reduce evaporation and which mulch suits blueberries?",
        "ground_truth": "Mulch reduces evaporation by up to 70%. Pine needles, applied 2-3 inches deep, are slightly acidifying "
                        "and best for acid-loving plants such as blueberries, azaleas and rhododendrons.",
    },
    {
        "question": "What temperature and light do tomato seedlings need to germinate and grow indoors?",
        "ground_truth": "Keep the temperature between 70-80°F (21-27°C) for germination, and provide 14-16 hours of light per "
                        "day under grow lights kept 2-3 inches above the seedlings.",
    },
    {
        "question": "How should I transplant tomato seedlings outdoors?",
        "ground_truth": "Harden off the seedlings over 7-10 days by gradually increasing outdoor exposure, plant deeply by "
                        "burying up to two-thirds of the stem, and space plants 24-36 inches apart. Soil should be at least "
                        "60°F (15°C).",
    },
    {
        "question": "What humidity and potting medium do orchids need, and how often should I repot?",
        "ground_truth": "Orchids prefer 50-70% humidity and need orchid bark mix, never regular potting soil, which suffocates "
                        "the roots. Repot every 1-2 years or when the bark has decomposed and no longer drains well.",
    },
    {
        "question": "When is garlic ready to harvest and how should it be cured?",
        "ground_truth": "Harvest when the lower third of the leaves have turned brown, typically June-July, after stopping "
                        "watering 2-3 weeks earlier. Cure in a warm, dry, well-ventilated area for 2-3 weeks, trim roots and "
                        "stems, then store in a cool, dark place.",
    },
    {
        "question": "What is the difference between hardneck and softneck garlic?",
        "ground_truth": "Hardneck garlic produces scapes, has a stronger flavor and fewer but larger cloves, and suits cold "
                        "climates. Softneck has no scapes, a milder flavor, more cloves per bulb, stores longer, is ideal for "
                        "braiding and suits mild climates.",
    },
    {
        "question": "How should I prune roses and when?",
        "ground_truth": "Prune in late winter or early spring, removing dead or crossing branches, and cut at a 45° angle above "
                        "an outward-facing bud. Deadhead spent blooms to encourage reblooming.",
    },
    {
        "question": "What are the symptoms of overwatering an orchid and how do I water it properly?",
        "ground_truth": "Overwatering is the most common cause of orchid death; brown, mushy roots indicate rot. Water once "
                        "every 7-10 days by putting the pot under lukewarm running water for 15-30 seconds, let it drain "
                        "completely and never leave it in standing water.",
    },
]
