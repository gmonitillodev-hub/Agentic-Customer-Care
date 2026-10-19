EVAL_DATASET = [
    # FAQ
    {
        "question": "Which payment methods does GreenThumb accept?",
        "ground_truth": "GreenThumb accepts Visa, Mastercard, American Express and Discover cards, PayPal and PayPal Credit, "
                        "Apple Pay and Google Pay, GreenThumb Gift Cards, and Affirm (buy now, pay later) on orders over $50.",
    },
    {
        "question": "I just placed an order by mistake. Can I still cancel it myself?",
        "ground_truth": "Within 1 hour of ordering you can modify or cancel the order directly from your account. After 1 hour "
                        "you must contact customer support as soon as possible, because changes cannot be guaranteed once the "
                        "order enters fulfillment.",
    },
    {
        "question": "How many rewards points do I need for a $5 reward and when do the points expire?",
        "ground_truth": "You earn 1 point per $1 spent and 100 points equal a $5 reward applied to your next order. Points "
                        "expire after 12 months of account inactivity.",
    },
    {
        "question": "Can I pay with more than one gift card, and can I get my money back from a gift card?",
        "ground_truth": "Yes, up to 3 gift cards can be combined per order and any remaining balance stays on the card. Gift "
                        "cards are non-refundable and cannot be exchanged for cash, except where required by law.",
    },
    {
        "question": "I forgot my password, how long is the reset link valid?",
        "ground_truth": "Click \"Forgot Password\" on the login page and a reset link is sent to your registered email. The "
                        "link expires in 24 hours.",
    },
    {
        "question": "What are the customer support phone number and opening hours?",
        "ground_truth": "Call 1-800-555-GROW (4769), Monday to Friday 8 AM - 6 PM EST and Saturday 9 AM - 1 PM EST. "
                        "Email is support@greenthumb.com, usually answered within 24 hours.",
    },
    # POLICIES
    {
        "question": "Can I return a packet of seeds that I have already opened?",
        "ground_truth": "No. Opened seed packets are not eligible for return, while unopened packets can be returned within "
                        "30 days. If GreenThumb-branded seeds fail to germinate under proper conditions, contact support "
                        "because they are covered by a germination guarantee.",
    },
    {
        "question": "How long do refunds take and is there a restocking fee?",
        "ground_truth": "Refunds are processed within 5-7 business days after the returned item is received and inspected, "
                        "to the original payment method. A 15% restocking fee may apply to large or heavy items such as power "
                        "tools and bulk soil orders. Original shipping charges are non-refundable unless the return is due to "
                        "GreenThumb's error or a defective product.",
    },
    {
        "question": "My plant arrived dead because of shipping. What do I have to do?",
        "ground_truth": "Report the issue within 48 hours of delivery with clear photos of the damaged plant and of the "
                        "packaging, via plantcare@greenthumb.com or 1-800-555-GROW. You can choose a free replacement or a "
                        "full refund.",
    },
    {
        "question": "My plant got pests three weeks after delivery even though I followed the care card. Am I covered?",
        "ground_truth": "Yes, the 30-Day Health Guarantee covers disease, pest infestation or failure to thrive within 30 days "
                        "of delivery despite following care instructions. You get a one-time replacement or store credit. "
                        "You must describe the care provided and send photos; the horticulture team may offer care advice first.",
    },
    {
        "question": "Does the plant guarantee cover frost damage after the plant was delivered?",
        "ground_truth": "No. Environmental damage such as frost after delivery, pet damage, accidental breakage or herbicide "
                        "exposure is not covered, nor are neglect or improper care, natural dormancy or cosmetic issues.",
    },
    {
        "question": "What are the shipping options, delivery times and costs?",
        "ground_truth": "Standard: 5-7 business days, free over $50 otherwise $5.99. Expedited: 2-3 business days, $12.99. "
                        "Express: 1-2 business days, $24.99. Freight (oversized): 7-14 business days, calculated at checkout. "
                        "Processing typically takes 1-2 business days.",
    },
    {
        "question": "I ordered a live plant on Thursday. When will it ship?",
        "ground_truth": "Live plants ship Monday through Wednesday only. Orders containing live plants placed after "
                        "Wednesday at 2 PM EST ship the following Monday.",
    },
    {
        "question": "Do you deliver to Hawaii or outside the United States?",
        "ground_truth": "No international shipping is available. GreenThumb ships within the contiguous US (48 states). "
                        "Alaska, Hawaii and U.S. territories have limited availability and additional shipping charges may apply, and live plants "
                        "cannot be shipped there.",
    },
    {
        "question": "What is the warranty period of a battery-powered tool and its lithium-ion battery?",
        "ground_truth": "Power tools (electric/battery mowers, trimmers, tillers, blowers) have a 2-year warranty. "
                        "Lithium-ion batteries are covered for 2 years or 500 charge cycles, whichever comes first.",
    },
    {
        "question": "How do I file a warranty claim for a defective tool?",
        "ground_truth": "Contact warranty@greenthumb.com or 1-800-555-GROW with your order number, date of purchase and a "
                        "description of the defect with clear photos. The claim is reviewed within 3-5 business days. If "
                        "approved the item is replaced (preferred), repaired for free, or a store credit/refund is issued.",
    },
    # PLATFORM ERRORS
    {
        "question": "What does error ERR009 mean and how should it be handled?",
        "ground_truth": "ERR009 is \"Payment declined by bank\". Ask the user to verify the card details and available funds, "
                        "try a different payment method, or contact their bank.",
    },
    {
        "question": "What is the recommended solution for ERR001?",
        "ground_truth": "ERR001 is a payment gateway timeout. Check the payment gateway service status and credentials, retry "
                        "the transaction after a few minutes, and contact the payment provider if the problem persists.",
    },
    {
        "question": "A customer says their discount code is rejected at checkout. Which error is it and what to check?",
        "ground_truth": "It is ERR002, invalid coupon code. Verify the coupon's validity, expiration date and usage limits, "
                        "and inform the user if the coupon is not applicable to their cart.",
    },
    {
        "question": "The customer never received the order confirmation email. What should support do?",
        "ground_truth": "This is ERR008, order confirmation email not sent. Check the email service integration and error "
                        "logs, resend the confirmation manually if needed, and advise the user to check spam/junk folders.",
    },
    {
        "question": "The shopping cart shows different content after the user switches device. Which error is this?",
        "ground_truth": "ERR005, cart synchronization error. Check session and user token validity, make sure the cart state "
                        "is updated client-side and server-side, and prompt the user to refresh the page or log in again.",
    },
    # GARDEN INFO
    {
        "question": "My compost pile is slimy and smells bad. What went wrong and how do I fix it?",
        "ground_truth": "The pile is too wet or has too many greens, so it has become anaerobic. Add browns and turn the pile. "
                        "The ideal ratio is about 3 parts browns to 1 part greens by volume, moist like a wrung-out sponge.",
    },
    {
        "question": "If I start a compost pile in October, when will it be ready and how often should I turn it in cold weather?",
        "ground_truth": "A pile started in October can produce finished compost by April or May. In cold weather turn it less "
                        "often: once a month is enough, and keep burying kitchen scraps in the center.",
    },
    {
        "question": "What is the difference between bypass and anvil pruners?",
        "ground_truth": "Bypass pruners have two curved blades that slide past each other like scissors, making clean, precise "
                        "cuts best for live wood and green growth. Anvil pruners have one blade cutting down onto a flat "
                        "surface, better for dead wood but they can crush live stems.",
    },
    {
        "question": "I need to cut a 3-inch thick branch. Which tool should I use?",
        "ground_truth": "Use a pruning saw, which is for branches over 2 inches in diameter (folding, bow or curved-blade "
                        "saws). Hand pruners cut up to 3/4 inch and loppers 3/4 to 2 inches.",
    },
    {
        "question": "At what angle and how often should I sharpen my garden tools?",
        "ground_truth": "Sharpen at least twice per season, following the original bevel angle, typically 20-25 degrees. File "
                        "in one direction only (push strokes), use a flat mill file for shovels/hoes and a diamond file or "
                        "whetstone for pruners, then remove the burr on the back side.",
    },
    {
        "question": "What soil and watering does lavender need?",
        "ground_truth": "Lavender needs full sun (6-8 hours), well-drained slightly alkaline soil (pH 6.5-7.5) with lean soil, "
                        "no rich compost, and 12-18 inches spacing. It is drought-tolerant once established; overwatering is "
                        "the number one killer.",
    },
    {
        "question": "At what level should the graft union sit when planting a rose?",
        "ground_truth": "The graft union (the bulge near the base) should sit at or just above soil level. Dig a hole twice as "
                        "wide and just as deep as the root ball, mix compost into the soil, then apply 2-3 inches of mulch "
                        "away from the stem.",
    },
    {
        "question": "What size pot and which variety are best for growing strawberries on a balcony?",
        "ground_truth": "Use pots at least 10-12 inches wide and 8 inches deep with drainage holes (one plant per 10-inch pot). "
                        "Day-neutral varieties are ideal for containers; recommended are 'Albion', 'Seascape', 'Tristar' and "
                        "'Mara des Bois'.",
    },
    {
        "question": "How deep and how far apart should I sow sunflower seeds, and when?",
        "ground_truth": "Sow directly after all frost danger has passed and soil reaches 50°F (10°C), 1 inch deep and 6 inches "
                        "apart. Thin seedlings to 12-24 inches apart once they have two sets of true leaves.",
    },
    {
        "question": "When and how do I start tomatoes from seed indoors?",
        "ground_truth": "Start 6-8 weeks before the last expected frost. Sow seeds 1/4 inch deep, 1 inch apart in seed-starting "
                        "mix, keep at 70-80°F (21-27°C) for germination, and give 14-16 hours of light with grow lights 2-3 "
                        "inches above the seedlings.",
    },
    {
        "question": "How much of an indoor herb can I harvest at once, and which herb needs its own pot?",
        "ground_truth": "Start harvesting once the plant has 6-8 sets of leaves and never remove more than one-third of the "
                        "plant at a time. Mint is extremely vigorous and should always be grown in its own container.",
    },
    {
        "question": "Which irrigation method is the most water-efficient and how much does a basic kit cost?",
        "ground_truth": "Drip irrigation is the most water-efficient (90%+ efficiency) and a basic DIY kit costs $50-$200. "
                        "Its emitters can clog, especially with hard water.",
    },
    {
        "question": "How thick should a straw mulch layer be and why use straw instead of hay?",
        "ground_truth": "Apply straw 4-6 inches deep because it compresses; it suits vegetable gardens, strawberry beds and "
                        "garlic. Use straw, not hay, because hay contains weed seeds.",
    },
    {
        "question": "How often and how should I water a Phalaenopsis orchid?",
        "ground_truth": "Water once every 7-10 days (more in summer, less in winter) by placing the pot under lukewarm "
                        "running water for 15-30 seconds and letting it drain completely. Never leave it in standing water; "
                        "overwatering is the most common cause of orchid death.",
    },
    {
        "question": "What are the NPK values of bone meal and blood meal and what are they used for?",
        "ground_truth": "Bone meal is 3-15-0, a phosphorus source for root growth and flowering, ideal for bulbs and "
                        "transplants. Blood meal is 12-0-0, a fast-acting nitrogen source for leafy vegetables that can burn "
                        "plants if overused.",
    },
    {
        "question": "When should I start pepper seeds and at what temperature do they germinate?",
        "ground_truth": "Start indoors 8-10 weeks before the last frost. Germination temperature is 80-85°F (27-29°C), best "
                        "with a heat mat, and takes 7-21 days. Transplant when night temperatures stay above 55°F (13°C), "
                        "spacing plants 18-24 inches apart.",
    },
    {
        "question": "How hot is a habanero compared to a jalapeño in SHU?",
        "ground_truth": "Jalapeño has medium heat at 2,500-8,000 SHU and is very productive. Habanero is very hot at "
                        "100,000-350,000 SHU with a fruity flavor.",
    },
    {
        "question": "When and how should I plant garlic cloves?",
        "ground_truth": "Plant in fall (typically October-November), 4-6 weeks before the ground freezes. Plant cloves pointed "
                        "end up, 2 inches deep and 6 inches apart in rows 12 inches apart, then mulch with 4-6 inches of straw "
                        "or shredded leaves.",
    },
    {
        "question": "Why can't I use garden soil in pots, and which mix is right for succulents?",
        "ground_truth": "Garden soil compacts heavily in containers, drains poorly, and may contain weed seeds, pests and "
                        "diseases. Succulents need a cactus and succulent mix with extra perlite and sand for fast drainage.",
    },
    {
        "question": "What gardening tasks should I do in March according to the planting calendar?",
        "ground_truth": "Indoors start tomatoes, peppers, eggplant and herbs 6-8 weeks before last frost. Outdoors, if the soil "
                        "is workable, direct sow peas, spinach and fava beans and plant bare-root roses, trees and berry bushes. "
                        "Also turn the compost pile and prepare raised beds with fresh compost.",
    },
    {
        "question": "Which soil pH do blueberries prefer, and what happens when the pH is too high?",
        "ground_truth": "Blueberries and other acid-loving plants (azaleas, rhododendrons) prefer pH 4.5-5.5. At high (alkaline) "
                        "pH, iron, manganese and zinc become unavailable, causing chlorosis (yellowing leaves).",
    },
    {
        "question": "What planting depth and spacing do tulips, daffodils and crocus need?",
        "ground_truth": "Tulips: 6-8 inches deep, 4-6 inches apart. Daffodils: 6-8 inches deep, 6-8 inches apart. Crocus: 3-4 "
                        "inches deep, 2-3 inches apart. Plant September through November when soil is below 60°F (15°C).",
    },
    {
        "question": "What should I do in the garden once the last frost has passed in spring?",
        "ground_truth": "Transplant warm-season seedlings (tomatoes, peppers, squash, cucumbers), direct sow beans, corn, "
                        "sunflowers and zinnias, install drip lines and soaker hoses, apply 2-3 inches of fresh mulch and set "
                        "up supports like tomato cages and trellises.",
    },
    {
        "question": "How do I water a succulent and how can I tell I am overwatering it?",
        "ground_truth": "Use the soak and dry method: water thoroughly until it drains, then let the soil dry completely. "
                        "Water every 7-14 days in summer and every 3-4 weeks in winter. Mushy, translucent leaves signal "
                        "overwatering or root rot.",
    },
    {
        "question": "What is the best time of day to water in summer and how much water per week?",
        "ground_truth": "Water early in the morning (6-10 AM) and avoid midday. Most gardens need 1-1.5 inches of water per "
                        "week in summer, delivered deeply and infrequently rather than in shallow daily sprinklings.",
    },
    {
        "question": "What are the pros and cons of clay soil and which plants suit it?",
        "ground_truth": "Clay soil is rich in nutrients and retains moisture, but drains poorly, warms slowly in spring and "
                        "compacts easily. It suits roses, asters, fruit trees and many ornamental shrubs.",
    },
    {
        "question": "What are the ideal dimensions for a vegetable raised bed?",
        "ground_truth": "Width 3-4 feet so you can reach the center, length 6-8 feet is most common, and depth at least 10-12 "
                        "inches (18-24 inches for deep-rooted crops like carrots and tomatoes).",
    },
    {
        "question": "How can I protect my garden plants from a hard frost?",
        "ground_truth": "Hard frost is below 28°F (-2°C). Use frost blankets or row covers (4-8°F of protection), apply 4-6 "
                        "inches of mulch after the ground freezes, and water the ground thoroughly before the freeze. Never "
                        "put plastic directly on plants because it conducts cold and causes freeze damage.",
    },
    {
        "question": "At what temperature should tropical plants be moved indoors in autumn, and which cover crops can I sow?",
        "ground_truth": "Bring tropical plants indoors before nighttime temperatures dip below 50°F (10°C). Plant a cover crop "
                        "such as winter rye, crimson clover or field peas in empty vegetable beds to prevent erosion and add "
                        "nutrients.",
    },
]
