import streamlit as st
import json
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import streamlit as st
from PIL import Image
import numpy as np
import os
import tempfile
import torch
import torchvision.transforms as transforms
import tensorflow as tf
import cv2

# --- PRODUCTS DATA ---
# (Paste your products_data list here)
products_data = [
    {
    "product_id": 1,
    "product_category": "Top",
    "product_subcategory": "Peplum Top",
    "product_sizes": ["S", "M", "L", "XL"],
    "product_image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcQT0LlikCStEITejYeOC4BxYvPtXMGLaRD5mJreptBzGou-Fr_dCZFjpLhMsYcBTKXJX8ILEWBXs6O1tsoxRmyk8XuolNliqF4yX-viYjQ",
    "fabric": "Cotton",
    "color": "Pink",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 2,
    "product_category": "Top",
    "product_subcategory": "Belted Shirt",
    "product_sizes": ["M", "L", "XL"],
    "product_image": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcTiyTJYnXzPywrB76MslrxAIN6QEREJgfQNqLsfCURuneIrLCK5e-Pre7i9sye_QzwR8X- tdQA5vnwJXWWlzJE0vkskUX7RJwXcZc0VI2uODe6an4xyCgRh6gg",
    "fabric": "Denim",
    "color": "White",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 3,
    "product_category": "Top",
    "product_subcategory": "Ruffled Layered Top",
    "product_sizes": ["XS", "S", "M", "L"],
    "product_image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcSMK3xB1t9nWsL3S3rnn442zCcsQ0sWSWuTNecwyjpVOPe2hLXyy3vuCgooe7w7v9CfqFS13jnCE3NToqcmyiby6Zlh9CCGNIdwrYsak6xz0bct5jLn4pUEMNL6-QRR_V8a9FK2KDU&usqp=CAc",
    "fabric": "Georgette",
    "color": "Marrom",
    "occasion": ["partwear"]
  },
  {
    "product_id": 4,
    "product_category": "Bottom",
    "product_subcategory": "Flared Jeans",
    "product_sizes": ["28", "30", "32", "34"],
    "product_image": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcTpGLmiXvP9O455QZ9a5lieGJGoCrnxfbBybJkxJybkZiNiyVMO6Eh_jM7WVWYoaY-qXAYYYw7wekJXsUzTRJMnvxMki2RmdLt3_SpF_ceT",
    "fabric": "Denim",
    "color": "Pink",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 5,
    "product_category": "Bottom",
    "product_subcategory": "A-line Skirt",
    "product_sizes": ["S", "M", "L"],
    "product_image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcTPYL4Y51jYp3yLyc979TaE3BVkKLQothwFs7btprakVoFRatrd8HXKWAyD171memXO6AEjBbasxWdUV_yb8jPciaVu4stn6wZHgihuQ6A",
    "fabric": "Cotton",
    "color": "Blue",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 6,
    "product_category": "Bottom",
    "product_subcategory": "Pleated Skirt",
    "product_sizes": ["M", "L", "XL"],
    "product_image": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcRDar5k6s9DNemXPAM_9V5tmgBje4nRcyc-d2hK18IhS11Yxj1DJorq7T3UfmT3bie7lPKh5jKrO1_pZvprVByalFoYiuwoDPQmligUURUU",
    "fabric": "Polyester",
    "color": "Black",
    "occasion": ["formal", "partwear"]
  },
  {
    "product_id": 7,
    "product_category": "Dress",
    "product_subcategory": "Wrap Dress",
    "product_sizes": ["S", "M", "L", "XL"],
    "product_image": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcSiAUgxT_3E0Adf-gVQ5fwxCysGDiKJbP3MgUSemvlKv4_B_Mxyp2NuYoF-7vqJav2yA88OEyoa7hi-hihO08bhpTwdbqjdssbefi6Z7q9ABAvuYKSrVLhqYts",
    "fabric": "Rayon",
    "color": "Pink",
    "occasion": ["partwear"]
  },
  {
    "product_id": 8,
    "product_category": "Dress",
    "product_subcategory": "Belted Dress",
    "product_sizes": ["XS", "S", "M", "L"],
    "product_image": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcTboIwcHyl9_YLNAnCMEBoTNXbusqgIenldOESFv9Empv6e5hrkMB9zWn8cFXZCSo9ZRcVFkLt-L8S74W3z5MPkrmyMpKREvPtcYMXujQA3Y4V_MVlvA36p3uNv2jjvq_8UJIWaeA&usqp=CAc",
    "fabric": "Linen",
    "color": "White",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 9,
    "product_category": "Dress",
    "product_subcategory": "Fit-and-Flare Dress",
    "product_sizes": ["M", "L", "XL"],
    "product_image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcRrwi9xEDnnWQEfV1I8dykQU_0PRThJMVCGOfPnCZ2TT0nnECt8LS7i1o3yNQlvzOIVrWtSkeMrYMrXIVglQm74jrIiHmjqnvYc6FV4QY7K",
    "fabric": "Silk Blend",
    "color": "Black",
    "occasion": ["partwear"]
  },
  {
    "product_id": 10,
    "product_category": "Outerwear",
    "product_subcategory": "Structured Blazer",
    "product_sizes": ["S", "M", "L"],
    "product_image": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcQZnWKMySOyumLr36PTPaTqsJUErNaGs15VmI6PnypsV6jtNXdOtAGWmVEQCeiqNKdPaOy2F0IcnCdH-MGzyZqC8sZEy_BTjkkRoU0cQMgJvVh1TTvSqjev",
    "fabric": "Wool",
    "color": "Black",
    "occasion": ["formal"]
  },
  {
    "product_id": 11,
    "product_category": "Outerwear",
    "product_subcategory": "Waist Belt Jacket",
    "product_sizes": ["M", "L", "XL"],
    "product_image": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcTADvvO-h_Oiktp_M_d2aZ29JdVV1fmg0bE6vFeYCqgxQ4k9mC823xkET64deyMZiiDKofUK5HFkUvEJ2MlZ0AvFKEUk4hLrePvv-Yr9Zs",
    "fabric": "Leather",
    "color": "Green",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 12,
    "product_category": "Outerwear",
    "product_subcategory": "Cropped Blazer",
    "product_sizes": ["XS", "S", "M"],
    "product_image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcSqsXYq0XoL3rpAPu2fb7gYNDkg4eCy0Gl7IyO87Jgaw6-O79b7cPZF5RKkqlsCLmKrpuWTY5VKGmshVm8wmXiaPJBjllC1HuwX8oTLbQmEVez52jptlFyzZaI4EAPi4gpRvkoHGLk&usqp=CAc",
    "fabric": "Tweed",
    "color": "Black",
    "occasion": ["formal"]
  },
  {
    "product_id": 13,
    "product_category": "Top",
    "product_subcategory": "V-Neck Top",
    "product_sizes": ["S", "M", "L"],
    "product_image": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcRzQn7patMz_ogFuV9_9PrbQMd3qMZyjeXmT_YR_lhr8GBnWVCUvhWc_Udzlx6ohB2I4Z5-uxS_rYF9oa0lViPrIu7uast76zrqpLkJHPXr-ZEv4gWVl7FiK4s&usqp=CAc",
    "fabric": "Rayon",
    "color": "Maroom",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 14,
    "product_category": "Top",
    "product_subcategory": "Scoop Neck Blouse",
    "product_sizes": ["M", "L", "XL"],
    "product_image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcR9vsm-lC7rynMNyIJdHQRElQGZAtztA8q_1rhn3dEYW8X3it9U7QPTIRHXEyA33qyvVieLYvxT82m24sANyk7JTdRrfluND5snMhkC4Jdj65rukT7txcMR-eUL1_ygjwBxtYbxVnGEZuw&usqp=CAc",
    "fabric": "Crepe",
    "color": "White",
    "occasion": ["partwear"]
  },
  {
    "product_id": 15,
    "product_category": "Top",
    "product_subcategory": "Wrap Top",
    "product_sizes": ["XS", "S", "M"],
    "product_image": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcT3JKcw3z5kdWFemJQyW2dGNMBe1KdcM4pTGUToQP9cDnJ30CAgC5_Anmw6iODM0vaE5OD-JnuLeJAFxI6OZMekW9dYFkOEx9ICxdi2ls3uFZ1vmx2zaezy",
    "fabric": "Satin",
    "color": "Yellow",
    "occasion": ["partwear"]
  },
  {
    "product_id": 16,
    "product_category": "Bottom",
    "product_subcategory": "Wide-leg Pants",
    "product_sizes": ["28", "30", "32", "34"],
    "product_image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcRcSudd0EB5LQzA3BXUUAREDe5S-62PhD2Im7yEeP-nJCw0LUv-sratKk8BPfqOeelvmM4s_T7U_7nf-r_bIAdRXFX2ud2yDFZRHWaz5p0",
    "fabric": "Linen",
    "color": "Black",
    "occasion": ["formal"]
  },
  {
    "product_id": 17,
    "product_category": "Bottom",
    "product_subcategory": "A-line Skirt",
    "product_sizes": ["S", "M", "L"],
    "product_image": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcTpqepAS4oPDM5mY3lOOmshAeQiDkLDG8cuo05nOmzVMmp8YHHOsrCvT-I9_9BCX8rFo-amKmUBf1vPRUTstY7CcG6pbrljwL7fB9wV02fuaE6rBylr_Ws-PwvkamD4D3Uhswk9QgfBSg&usqp=CAc",
    "fabric": "Denim",
    "color": "Green",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 18,
    "product_category": "Bottom",
    "product_subcategory": "Palazzo Pants",
    "product_sizes": ["M", "L", "XL"],
    "product_image": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcQC21u9JItLY2DBdqLO7p5aTuwIHtQqtq39PB3Hk7LMqOum_dxdciFS-VfcndMmtaQ6RPvbLLmUiZF4F_lYjz8MEG4_Q9EbSDbhOal1IArm",
    "fabric": "Georgette",
    "color": "Blue",
    "occasion": ["formal"]
  },
  {
    "product_id": 19,
    "product_category": "Dress",
    "product_subcategory": "Fit-and-Flare Dress",
    "product_sizes": ["S", "M", "L", "XL"],
    "product_image": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcQ3-3QPMX3H9k5n8lt_SYG48iMeB5cqi0AiE0MjzV9qSPQ8Nws4Oiy7pAd1SZCJzDaim0rKQa_Ibi77I4iLgYuJ1VhjT_OF2k7cyQSV12_Fly-lDnstQTPqszi7Gy5hURqj6t-DinaRlXo&usqp=CAc",
    "fabric": "Polyester",
    "color": "White & Yellow",
    "occasion": ["partwear"]
  },
  {
    "product_id": 20,
    "product_category": "Dress",
    "product_subcategory": "A-Line Dress",
    "product_sizes": ["XS", "S", "M"],
    "product_image": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcQwkFEUwbJQtUoJeB8sosKDJT2nbq8U-bebgA_YajJNtSoAuOLSkYSj896ILWURv86l4o6lotXP8iD3eY7_3_W6goMJX_i_EJOMdhg1D49ka3Bluz4w0MkhVWzQS9K3UbqOhrzl-D_dEpeoFg&usqp=CAc",
    "fabric": "Cotton",
    "color": "Blue",
    "occasion": ["partwear"]
  },
  {
    "product_id": 21,
    "product_category": "Dress",
    "product_subcategory": "Bias-cut Dress",
    "product_sizes": ["M", "L"],
    "product_image": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcRxYUO27deowDTJCik-Rn8ApMnwbKlr9Ha0DspzAxeKRma9jQ1EiMKCYQPO8Mf0pWYsAdMLc8vPR3QXcgnaB53eglKJSyO7",
    "fabric": "Satin",
    "color": "Black",
    "occasion": ["partwear"]
  },
  {
    "product_id": 22,
    "product_category": "Outerwear",
    "product_subcategory": "Longline Jacket",
    "product_sizes": ["S", "M", "L"],
    "product_image": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcSpIHkQiGQZqChmbX8mJ0DUSAFNcVtd10GoAovKdtLQlEDfUfqSTaeatOc0M0se8Dw-B8CNz9CGZqlOAToED_pV8SG1dZirzdr17Gi0jb-D",
    "fabric": "Wool",
    "color": "Grey",
    "occasion": ["formal"]
  },
  {
    "product_id": 23,
    "product_category": "Outerwear",
    "product_subcategory": "Waterfall Cardigan",
    "product_sizes": ["M", "L", "XL"],
    "product_image": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcSS9ViUh4tM45338hmTBTP7dgB_pb_34TGIXPZcsFIQaXamSTRfzWNE-B_DUCZ_7Q8uDhYFbvECksCv6kDz1y_ICd80NTDMCvFF4JrfpBQ",
    "fabric": "Knit",
    "color": "White",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 24,
    "product_category": "Outerwear",
    "product_subcategory": "Slim Blazer",
    "product_sizes": ["XS", "S", "M"],
    "product_image": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcQ9qPutncX4ckE2B0iagjq0hPAr63AH_HL8LXItFlAiGief9tHwt36RdaAmqdbAQn54XYSTlF9AOiD-bmbUe8JiFAOLLgFd-n6jAaCGwpqMpykGTH27XyT7",
    "fabric": "Crepe",
    "color": "Black",
    "occasion": ["formal"]
  },
  {
    "product_id": 25,
    "product_category": "Top",
    "product_subcategory": "Wrap Blouse",
    "product_sizes": ["S", "M", "L"],
    "product_image": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcTlD6VEGPP13ik9cZU7rPmB2MjAUj9kjVK6LPGF1JvJkOos5mJC1L_3xBGBQiV3kR_sp2IC2CNJ1PAn3G-U-8gJ68p-a10he-7DVUdalxKU",
    "fabric": "Satin",
    "color": "Beinge",
    "occasion": ["partwear"]
  },
  {
    "product_id": 26,
    "product_category": "Top",
    "product_subcategory": "Fitted Crop Top",
    "product_sizes": ["XS", "S", "M"],
    "product_image": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcRzx_gEEaYhv73a3cqHI7rXHFgOyCopQja4uXRIzjoXOEp7AffnhqaohW3k8D6Zg7W4xr0CsH7D_2Pfd6Ztx3a2nKqeIS7-SwO9DSWV28M",
    "fabric": "Knit",
    "color": "White",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 27,
    "product_category": "Top",
    "product_subcategory": "Structured Shirt",
    "product_sizes": ["M", "L", "XL"],
    "product_image": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcQvN2kfQ9eoGY96NNfbPsjzWaC3twaddzU3vkCsIEkVZWj2T_hOawJoI46FPSJVHcvVgnfxMGJGpGagewVmUNgf_UiN1U2n4VJnT-yEDsHZsKsRHiUxQfzSkUh1&usqp=CAc",
    "fabric": "Cotton",
    "color": "Blue",
    "occasion": ["formal"]
  },
  {
    "product_id": 28,
    "product_category": "Bottom",
    "product_subcategory": "High-waist Jeans",
    "product_sizes": ["28", "30", "32", "34"],
    "product_image": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcQvhgIj_i3A9pCcn6jHJ6bJYBXy4dx9AVzmlBGDttRWRgN-BQl6Q1OlP1J-TKF0SZdFY583QAlWQOCqTqlhfM0ee7VUEvXKixAZbjW-OVc",
    "fabric": "Denim",
    "color": "Blue",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 29,
    "product_category": "Bottom",
    "product_subcategory": "Pencil Skirt",
    "product_sizes": ["S", "M", "L"],
    "product_image": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcQ-_tJT9ckKQKJSXEozJ-5lZsObnJAx7LWkGLY2Aza1jJgdihAvWatv2tFi2HniQwPKVToCvDNExKNi6dnur03f36X1KOdrVUC4LSsdaogj",
    "fabric": "Tweed",
    "color": "White",
    "occasion": ["formal"]
  },
  {
    "product_id": 30,
    "product_category": "Bottom",
    "product_subcategory": "Bodycon Skirt",
    "product_sizes": ["XS", "S", "M"],
    "product_image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcSj8wROmJnXHRBNpH97lc8_pK6fQmS5qGIaLgt03zwZvW-sD-C7j5bFptomyorgnHTiy4_SvjiaSWQvRP8dZdOfjE54lyaFj4g9I86vrZIPvoStAVwTDgWtXQ",
    "fabric": "Spandex",
    "color": "White",
    "occasion": ["partwear"]
  },
  {
    "product_id": 31,
    "product_category": "Dress",
    "product_subcategory": "Bodycon Dress",
    "product_sizes": ["S", "M", "L", "XL"],
    "product_image": "https://tse1.explicit.bing.net/th/id/OIP.yjWUJ9hEB1ATG36ihOKwywHaLG?r=0&rs=1&pid=ImgDetMain&o=7&rm=3",
    "fabric": "Spandex",
    "color": "Blue",
    "occasion": ["partwear"]
  },
  {
    "product_id": 32,
    "product_category": "Dress",
    "product_subcategory": "Sheath Dress",
    "product_sizes": ["M", "L"],
    "product_image": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcQtRMbUPqZk-IXPEsG4WcGcEvI_qcWZUCTYYw8LpuDX0P6-UrDJFsDvdYz1NNCJ2jLeJUmZLoQYxAt-akxBquqvcbCpmtEnoUwPb4R9vYfy6YxOrL39U2bV",
    "fabric": "Crepe",
    "color": "Red",
    "occasion": ["formal"]
  },
  {
    "product_id": 33,
    "product_category": "Dress",
    "product_subcategory": "Mermaid Gown",
    "product_sizes": ["S", "M", "L"],
    "product_image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcSUEFE0susoxXPHVDvs7PZvzPLFfqUjTqx1mrPjZB8r6yVqo9or6iRuG9INTuXcQFqmDQrJtJjiKoWfxUmZnCXBz_fdG7tiAK9gAsRbTGNe87gZshoYfesH",
    "fabric": "Silk",
    "color": "Red",
    "occasion": ["partwear"]
  },
  {
    "product_id": 34,
    "product_category": "Outerwear",
    "product_subcategory": "Belted Trench Coat",
    "product_sizes": ["S", "M", "L"],
    "product_image": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcTVzi49_ZdX1HQQoVlB93dr89JhHyi3yimglOySxXPa2lrTSm4K-cT3ghuy7-o6dLc_HGPbyh5hEKyuOLzY787EiI8a_oD6CXES0LxdQ1U",
    "fabric": "Cotton",
    "color": "Beige",
    "occasion": ["formal"]
  },
  {
    "product_id": 35,
    "product_category": "Outerwear",
    "product_subcategory": "Cropped Jacket",
    "product_sizes": ["XS", "S", "M"],
    "product_image": "https://tse3.mm.bing.net/th/id/OIP.7I30T0diWE8mJv00Bq7IOQHaJS?r=0&rs=1&pid=ImgDetMain&o=7&rm=3",
    "fabric": "Denim",
    "color": "Blue",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 36,
    "product_category": "Outerwear",
    "product_subcategory": "Fitted Blazer",
    "product_sizes": ["M", "L", "XL"],
    "product_image": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcQjjPKX2hHwC178tPVt_cvIx7z9jwqfT6O-o7HqeKuzoeLrB0B-RQ0e-RqSyQw-Ie8Tp4nSuMlrXEVfOvACvXKiHDemzROl-_uoRFBgxMwdx2phLmZ7sxoMWlopucW2EO-UKieEjueQ&usqp=CAc",
    "fabric": "Polyester",
    "color": "Blue",
    "occasion": ["formal"]
  },
  {
    "product_id": 37,
    "product_category": "Top",
    "product_subcategory": "Off-Shoulder Top",
    "product_sizes": ["S", "M", "L"],
    "product_image": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcSKYqv40fqi4DhtNlEhR1kTlZTlHt0_o7ODvJ3jC5hPdg4-uoWPhVwH5ijA4ZMyNtL708rkoF5xuoo1GfIot9gc4GjIEc_ShkY6TCPpsGTL0Dzpxan60xZwV2qPISm8yUbHpXrVbw&usqp=CAc",
    "fabric": "Cotton",
    "color": "Maroom",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 38,
    "product_category": "Top",
    "product_subcategory": "Boat Neck Blouse",
    "product_sizes": ["M", "L", "XL"],
    "product_image": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcT1aWF7Yumso4e_jVQThDy_SLv0DJkNo3pjG4bst4GTSIbgkJ_J7RQd0NnFbrMSJJkxeKkJpIPcbCjR80yqu0ZDrGWUbp22vSZq3XGr53AnD7P8XV8Zt68ONA",
    "fabric": "Silk Blend",
    "color": "Black",
    "occasion": ["partwear"]
  },
  {
    "product_id": 39,
    "product_category": "Top",
    "product_subcategory": "Puff Sleeve Shirt",
    "product_sizes": ["XS", "S", "M"],
    "product_image": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcTII_WTxibBHuGqusBqwvd_kz9v8jRwHvKokEvFp6W18SkgywaZxOOQKeWLE4l2sKFi8ihRTspl3RQn_lemwO0KHWGcYCi3_3qh1jSoFdeD",
    "fabric": "Organza",
    "color": "White",
    "occasion": ["partwear"]
  },
  {
    "product_id": 40,
    "product_category": "Bottom",
    "product_subcategory": "Straight-leg Pants",
    "product_sizes": ["28", "30", "32"],
    "product_image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcTYNKn1nFOpGZzFQWGVSnrVTpQjl4fpHTwQmGJc--DjtmUrWI1f55ArRi-TgQZji-2OVkL1WTWE_jLX0ChPaLh42ZFc7-SYzuM-UKORDLA",
    "fabric": "Cotton",
    "color": "Cream",
    "occasion": ["western_casual","formal"]
  },
  {
    "product_id": 41,
    "product_category": "Bottom",
    "product_subcategory": "Dark-colored Jeans",
    "product_sizes": ["28", "30", "32", "34"],
    "product_image": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcSMYOY2ypzPiqHrVGc45J70dxXmdV5jYvaoCR5q8HOxv-WX0P6J9Mw5jGGtcD5OmP4kRSBDU7Oi9GueMA6TEq-DYJAnL6lGwd4EaqCgMRd0ZKwRccIAeom9&usqp=CAc",
    "fabric": "Denim",
    "color": "Blue",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 42,
    "product_category": "Bottom",
    "product_subcategory": "A-line Skirt",
    "product_sizes": ["S", "M", "L"],
    "product_image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcQ6GfVFxvOvnfgg6GqSptPow-R3SFDzVuDEVDFAsY71NNYO3tvaEIgsJ89u_UuOQx3Y0u6wP5yib0ssyw1NT5STxQEeHCfkx83B2-h8uTnq",
    "fabric": "Wool",
    "color": "Black",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 43,
    "product_category": "Dress",
    "product_subcategory": "Empire Waist Dress",
    "product_sizes": ["S", "M", "L", "XL"],
    "product_image": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcTUDAGacWJNq2I6o65mV2RQWgE8FbQ6PmDXpWDMJIrFCfA77tV_pMU3qCFgSwm8IreVFop0xzKOtagnvYGYmLgsiXSG83YoXiOQexke1QRhJzV-DQUnyST0UQ",
    "fabric": "Chiffon",
    "color": "Green",
    "occasion": ["partwear"]
  },
  {
    "product_id": 44,
    "product_category": "Dress",
    "product_subcategory": "A-line Dress",
    "product_sizes": ["M", "L"],
    "product_image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcQwBfzJJxGXajKyq7qtdD2qNooXZSGAKGBn3GkymFUvFVk4L-FwexI1DkYm1FZke1tKmZnCwMSqdKhh6iJ1ANmxOf1C9xCXTtPl1iZDsQMDhVAkLaQkc36Fnw",
    "fabric": "Cotton",
    "color": "Black",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 45,
    "product_category": "Dress",
    "product_subcategory": "Fit-and-Flare Dress",
    "product_sizes": ["S", "M", "L"],
    "product_image": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcQSr0BFuLJ79QuQ75r8rGTLq0hbrnAFMx0EURxu3LbKE692y5KTs2s8ipsQUJbqksMNsuLxoH5-nvtnHx6mAGRNXeDrKs0MyAFPz3_nLHo_N1n3SBzYYJtnsQ",
    "fabric": "Viscose",
    "color": "Black",
    "occasion": ["partwear"]
  },
  {
    "product_id": 46,
    "product_category": "Outerwear",
    "product_subcategory": "Structured Shoulder Jacket",
    "product_sizes": ["S", "M", "L"],
    "product_image": "http://assets.myntassets.com/assets/images/33444572/2025/4/28/fe34711c-b5da-411c-a069-b20e6120c76c1745836340367-MANGO-Double-Breasted-Structured-Shoulder-Blazer-56517458363-1.jpg",
    "fabric": "Wool",
    "color": "White",
    "occasion": ["formal"]
  },
  {
    "product_id": 47,
    "product_category": "Outerwear",
    "product_subcategory": "Cropped Jacket",
    "product_sizes": ["XS", "S", "M"],
    "product_image": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcQQ46q6_-YalLr1wHXjv2cQfnOjqUWZQjZ36XliwEJXvsQjYxMVdWhVNsxbR1Ge4vSZBvOUJDW-eqa4PznoxPKO7WDR3P-96n5PClw2h-l6shqR40lMyp8fHg&usqp=CAc",
    "fabric": "Denim",
    "color": "Red",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 48,
    "product_category": "Outerwear",
    "product_subcategory": "Boxy Blazer",
    "product_sizes": ["M", "L", "XL"],
    "product_image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcSW_6IqfezC7JedyQuEiUej54Swx-UvEVFNkFbcD3A8b15PUX_rJb8XYwvqroQUJ3obXaUpJmUqUD3SwgRDDkPhqEJFj_O4EpdpfzWvziM4txslCH36NbDHJqdx4SXp8QTiyzJwjJk&usqp=CAc",
    "fabric": "Linen",
    "color": "Red",
    "occasion": ["formal"]
  },
  {
    "product_id": 49,
    "product_category": "Top",
    "product_subcategory": "V-neck Blouse",
    "product_sizes": ["S", "M", "L"],
    "product_image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcTGJvGiK696MslWc_2fPfggFQo317T0fpHmGKAs_4O_ugZjDyVo-pIBmR90AisH_WWltHzALJAHCA4oV6sXb70Y4a_yiFz70PvYg2bslTP_pYT-oNKO76qEKA",
    "fabric": "Chiffon",
    "color": "White",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 50,
    "product_category": "Top",
    "product_subcategory": "Flowy Wrap Top",
    "product_sizes": ["M", "L", "XL"],
    "product_image": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcS2SCm1W4QmacUq2OvuYnOdgttvGm_-2S1oQTw7FX3hYH6_ABt0m5XgbLbypYtfldiicdznKn97ys32-MxsRg340NQ7ujSwV4Q3SBuaU9W4",
    "fabric": "Georgette",
    "color": "Yellow",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 51,
    "product_category": "Top",
    "product_subcategory": "Longline Tunic",
    "product_sizes": ["L", "XL", "XXL"],
    "product_image": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcTZaQUSNMwPCCWkGcvvqIS-l854U98mNHTiNUupykPLrsAW6KXoKRwDDqNM3liFrppoVToznvEYs9iKtp4aHM0pGgJwFR9TG-nP-I4JWpIR_EcJA1kpF_v0dQA1pABG_xiFC9SR7A&usqp=CAc",
    "fabric": "Cotton",
    "color": "Green",
    "occasion": ["formal"]
  },
  {
    "product_id": 52,
    "product_category": "Bottom",
    "product_subcategory": "Straight Pants",
    "product_sizes": ["28", "30", "32"],
    "product_image": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcTrvyxK4XG2Bv3H8qJnS5aAWwxk6D6KXR306pJT38hVXxn4YDrkZKj5BinoqNMQfTFF2S0sr2Qx_NyRFxx9bwUAl0nG2JH9-UKi6lU6tV8MQkSwcC06Wy1R&usqp=CAc",
    "fabric": "Denim",
    "color": "Black",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 53,
    "product_category": "Bottom",
    "product_subcategory": "Bootcut Pants",
    "product_sizes": ["28", "30", "32", "34"],
    "product_image": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcTgFKIGZuGOO1zHaUa7zsWXC6hVIag24MPWXjoeG-qdU_UPD-MSgx_OdiZSSRadRnmpZA9F-NL1omwrs4-83ap8S-Sxv0q18nYPdpm47os",
    "fabric": "Corduroy",
    "color": "Blue",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 54,
    "product_category": "Bottom",
    "product_subcategory": "High-waist Skirt",
    "product_sizes": ["S", "M", "L"],
    "product_image": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcSX-RnaoyVBuCZWOwnB11Qrm4kkjEO9kwj-TpBtk_q9b-Elptu2sHVRwWFSu4UOYfNFLGnmE5IXOauzKN6eHkQtDn6ODDQKIJXKZ2ympgtp",
    "fabric": "Cotton",
    "color": "Black",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 55,
    "product_category": "Dress",
    "product_subcategory": "Empire Waist Dress",
    "product_sizes": ["S", "M", "L", "XL"],
    "product_image": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcQ3O6VcIPuBYw57iR7FkrZ2X6xqOWAOvE2RV7lQnD4LR7P4ahM4RK1MwgjQQKekabaxMVy-WzdRpe1L82sGq5SGxkngMRjAM9-wsd_fl3k",
    "fabric": "Rayon",
    "color": "Black",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 56,
    "product_category": "Dress",
    "product_subcategory": "A-line Dress",
    "product_sizes": ["M", "L"],
    "product_image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcROcK5hd9jTph1B5sf06IqBx5GlSPwzPu_3HehmzQoK_OjdlMM20gyME9lg9M5HYnuMFbY-TqdfgP3FN7B5KycctnHP7TMrpWvWmpFyyd8FMdq1i50hXPCb",
    "fabric": "Silk Blend",
    "color": "Yellow",
    "occasion": ["partwear"]
  },
  {
    "product_id": 57,
    "product_category": "Dress",
    "product_subcategory": "Wrap Dress",
    "product_sizes": ["S", "M", "L"],
    "product_image": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcRhwk0RLT6wfz44kEY-Z0ti8wvgfta027p-XbceTPpFK4XpavDvgw1wxQ1hthsGKKRSsF6FqKWloLDBpSZ4n9sw-qyypoHqt90zOaJn8ChW",
    "fabric": "Georgette",
    "color": "Green",
    "occasion": ["partwear"]
  },
  {
    "product_id": 58,
    "product_category": "Outerwear",
    "product_subcategory": "Open-front Cardigan",
    "product_sizes": ["S", "M", "L"],
    "product_image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcQ3wa8Pudv5WckcAnVkDaep_260gecp2szM5hJuWjIOQP_0UN4rOtDyQjB0VqHJkdU3vHKzNuNJv-MMd9UDfJ4HFlEbgQdJgkO5Mna2r0cbYImJ51t9ZiYc",
    "fabric": "Knit",
    "color": "Pink",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 59,
    "product_category": "Outerwear",
    "product_subcategory": "Longline Vest",
    "product_sizes": ["M", "L", "XL"],
    "product_image": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcRLjGE82Tt2457eXNmI9Q6ZSsMwnTALALR3i4739uPERilwsR2phrBi3hkDNcsysKRv0hfuG0P0czn2PvInwc13KVobiNfn_YIG72W5LjjR",
    "fabric": "Linen",
    "color": "Beige",
    "occasion": ["western_casual"]
  },
  {
    "product_id": 60,
    "product_category": "Outerwear",
    "product_subcategory": "Blazer with Single Button",
    "product_sizes": ["L", "XL", "XXL"],
    "product_image": "https://images.meesho.com/images/products/440006300/fxdjy_512.webp?width=512",
    "fabric": "Polyester",
    "color": "Black",
    "occasion": ["formal"]
  },
  {
    "product_id": 61,
    "product_category":"Outerwear",
    "product_subcategory":"Anarkali Suits",
    "product_sizes": ["L", "XL", "XXL"],
    "product_image":"https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcSit-KFEGZkABWCMsZSwvuSLQ_kNiAr8ygfsMqFSy6k4LIXYcqVJR5nY9cDXk_DNxVLX-MBg_nc2dLZCNMmrpSzDxAxbgxun9zpc7g1YqM",
    "fabric": "Cotton",
    "color": "Blue",
    "occasion": ["ethenic"]
  },
  {
    "product_id": 62,
    "product_category":"Outerwear",
    "product_subcategory":"Lehengas",
    "product_sizes": ["L", "XL", "XXL"],
    "product_image":"https://www.google.com/imgres?q=Lehengas%3A%20Opt%20for%20a%20flared%20or%20A-line%20lehenga%20with%20a%20well-fitted%20choli%20that%20has%20a%20scoop%20or%20boat%20neck%20to%20add%20volume%20to%20the%20upper%20body.&imgurl=https%3A%2F%2Fmedia.samyakk.com%2Fpub%2Fmedia%2Fcatalog%2Fproduct%2Fc%2Fr%2Fcream-mermaid-style-net-designer-lehenga-with-pentagon-neck-blouse-gg1159-b.jpg&imgrefurl=https%3A%2F%2Fwww.samyakk.com%2Fblog%2Fperfect-lehenga-guide-every-body-type%2F%3Fsrsltid%3DAfmBOooAXCzv7i64pDtBtonF2r_9arGNpMM2MRt6F92r7H13gUxrid7s&docid=FBe3jGKwUvyS1M&tbnid=X5HrtGq6o9d8SM&vet=12ahUKEwj2qqD1yuKPAxXwcvUHHYV6IpYQM3oECBoQAA..i&w=1200&h=1800&hcb=2&ved=2ahUKEwj2qqD1yuKPAxXwcvUHHYV6IpYQM3oECBoQAA",
    "fabric": "Cotton",
    "color": "Gold",
    "occasion": ["ethenic"]
  },
    {
    "product_id": 63,
    "product_category":"Outerwear",
    "product_subcategory":"Sarees",
    "product_sizes": ["L", "XL", "XXL"],
    "product_image":"https://cdn.shopify.com/s/files/1/0588/3812/2548/files/AStitchofSummer-3_f4af9706-b350-4f27-b855-198f0f14b9dc.png?v=1749210856",
    "fabric": "Cotton",
    "color": "Gold",
    "occasion": ["ethenic"]
  },
  {
    "product_id": 64,
    "product_category":"Outerwear",
    "product_subcategory":"Kurtas and Tunics",
    "product_sizes": ["L", "XL", "XXL"],
    "product_image":"https://cdn.shopify.com/s/files/1/0586/9207/5703/files/02_cd850812-3373-4e32-b536-e8d52df6aca4.jpg?v=1721626719",
    "fabric": "Cotton",
    "color": "Gold",
    "occasion": ["ethenic"]
  },
  {
    "product_id": 66,
    "product_category":"Outerwear",
    "product_subcategory":"Kurtas and Tunics",
    "product_sizes": ["L", "XL", "XXL"],
    "product_image":"https://cdn.shopify.com/s/files/1/0586/9207/5703/files/02_cd850812-3373-4e32-b536-e8d52df6aca4.jpg?v=1721626719",
    "fabric": "Cotton",
    "color": "Gold",
    "occasion": ["ethenic"]
  },
  {
    "product_id": 65,
    "product_category":"Outerwear",
    "product_subcategory":"Anarkali Suits",
    "product_sizes": ["L", "XL", "XXL"],
    "product_image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSnIl8CYg1uqSlwgBfZNWqVGB2X0Xoq15qnsg&s",
    "fabric": "Cotton",
    "color": "Red",
    "occasion": ["ethenic"]
  },
  {
    "product_id": 66,
    "product_category":"Outerwear",
    "product_subcategory":"Lehengas",
    "product_sizes": ["L", "XL", "XXL"],
    "product_image":"https://www.cdnensemble.xyz/pub/media/catalog/product/cache/391a5e1abf666a8c41861a6cd6227bf9/r/m/rmct-15-1_1.jpg",
    "fabric": "Cotton",
    "color": "Black",
    "occasion": ["ethenic"]
  },
  {
    "product_id": 67,
    "product_category":"Outerwear",
    "product_subcategory":"Kurtas and Tunics",
    "product_sizes": ["L", "XL", "XXL"],
    "product_image":"https://assets.myntassets.com/dpr_1.5,q_30,w_400,c_limit,fl_progressive/assets/images/2025/JANUARY/7/whvMDXUp_5a44617011294678b1408e33e3de7f70.jpg",
    "fabric": "Cotton",
    "color": "Purple",
    "occasion": ["ethenic"]
  },
    {
    "product_id":68,
    "product_category":"Outerwear",
    "product_subcategory":"Kurtas and Tunics",
    "product_sizes": ["L", "XL", "XXL"],
    "product_image":"https://i.pinimg.com/736x/68/f6/9e/68f69eac27416d8b45f7c53c200e5121.jpg",
    "fabric": "Cotton",
    "color": "Blue",
    "occasion": ["ethenic"]
  },
  {
    "product_id":69,
    "product_category":"Outerwear",
    "product_subcategory":"Saree",
    "product_sizes": ["L", "XL", "XXL"],
    "product_image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQtpYv8nHf6ywc9ywJ94mdRuXnfWGWBDVfDdw&s",
    "fabric": "Cotton",
    "color": "Blue",
    "occasion": ["ethenic"]
  },
  {
    "product_id":70,
    "product_category":"Outerwear",
    "product_subcategory":"Saree",
    "product_sizes": ["L", "XL", "XXL"],
    "product_image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRUezVfdj6bH1M08KYOCc5BDNPIdnEf0lOHAg&s",
    "fabric": "Cotton",
    "color": "Blue",
    "occasion": ["ethenic"]
  }
]
# --- RECOMMENDATION LOGIC ---
def get_recommendations_by_body_shape(data, body_shape, selected_fabrics=None, selected_occasions=None, selected_subcategories=None, selected_categories=None):
    """
    Recommends clothing items based on a given body shape and additional filters.
    """
    # Rules for each body shape
    rules = {
        "Rectangle": {
            "Top": ["Peplum Top", "Belted Shirt", "Ruffled Layered Top"],
            "Bottom": ["Flared Jeans", "A-line Skirt", "Pleated Skirt"],
            "Dress": ["Wrap Dress", "Belted Dress", "Fit-and-Flare Dress", "Saree", "Anarkali Suits", "Lehengas"],
            "Outerwear": ["Structured Blazer", "Waist Belt Jacket", "Cropped Blazer"],
            "fabrics": ["Cotton", "Linen", "Polyester", "Wool", "Denim"]
        },
        "Inverted Triangle": {
            "Top": ["V-Neck Top", "Scoop Neck Blouse", "Wrap Top"],
            "Bottom": ["Wide-leg Pants", "A-line Skirt", "Palazzo Pants"],
            "Dress": ["Fit-and-Flare Dress", "A-Line Dress", "Bias-cut Dress", "Saree", "Kurtas and Tunics", "Anarkali Suits", "Lehengas"],
            "Outerwear": ["Longline Jacket", "Waterfall Cardigan", "Slim Blazer"],
            "fabrics": ["Rayon", "Crepe", "Satin", "Georgette", "Silk Blend"]
        },
        "Hourglass": {
            "Top": ["Wrap Blouse", "Fitted Crop Top", "Structured Shirt"],
            "Bottom": ["High-waist Jeans", "Pencil Skirt", "Bodycon Skirt"],
            "Dress": ["Bodycon Dress", "Sheath Dress", "Mermaid Gown", "Saree", "Anarkali Suits", "Lehengas"],
            "Outerwear": ["Belted Trench Coat", "Cropped Jacket", "Fitted Blazer"],
            "fabrics": ["Spandex", "Denim", "Tweed", "Silk Blend", "Cotton"]
        },
        "Pear": {
            "Top": ["Off-Shoulder Top", "Boat Neck Blouse", "Puff Sleeve Shirt"],
            "Bottom": ["Straight-leg Pants", "Dark-colored Jeans", "A-line Skirt"],
            "Dress": ["Empire Waist Dress", "A-line Dress", "Fit-and-Flare Dress", "Saree", "Anarkali Suits", "Lehengas"],
            "Outerwear": ["Structured Shoulder Jacket", "Cropped Jacket", "Boxy Blazer"],
            "fabrics": ["Cotton", "Wool", "Denim", "Linen", "Organza"]
        },
        "Apple": {
            "Top": ["V-neck Blouse", "Flowy Wrap Top", "Longline Tunic"],
            "Bottom": ["Straight Pants", "Bootcut Pants", "High-waist Skirt"],
            "Dress": ["Empire Waist Dress", "A-line Dress", "Wrap Dress", "Saree", "Kurtas and Tunics", "Anarkali Suits"],
            "Outerwear": ["Open-front Cardigan", "Longline Vest", "Blazer with Single Button"],
            "fabrics": ["Chiffon", "Georgette", "Rayon", "Viscose", "Knit"]
        }
    }

    if body_shape not in rules:
        return f"Error: No rules found for body shape '{body_shape}'."

    # Step 1: Get initial recommendations based on body shape rules
    recommended_subcategories = []
    for category, subcategories in rules[body_shape].items():
        if category != "fabrics":
            recommended_subcategories.extend(subcategories)
    
    body_shape_recommendations = [
        product for product in data if product["product_subcategory"] in recommended_subcategories
    ]

    # Step 2: Apply additional filters if selected by the user
    filtered_recommendations = body_shape_recommendations

    if selected_categories:
        filtered_recommendations = [p for p in filtered_recommendations if p['product_category'] in selected_categories]

    if selected_subcategories:
        filtered_recommendations = [p for p in filtered_recommendations if p['product_subcategory'] in selected_subcategories]

    if selected_fabrics:
        filtered_recommendations = [p for p in filtered_recommendations if p['fabric'] in selected_fabrics]

    if selected_occasions:
        filtered_recommendations = [
            p for p in filtered_recommendations if any(item in p['occasion'] for item in selected_occasions)
        ]
            
    return filtered_recommendations

# --- MODEL AND PREDICTION LOGIC ---
@st.cache_resource
def load_the_model():
    try:
        model = load_model('body_shape_model_simplex.h5')
        return model
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        return None

# Load the model
model = load_the_model()

# Class labels for your model's output
class_labels = {
    0: "Rectangle",
    1: "Inverted Triangle",
    2: "Hourglass",
    3: "Apple"
}
u2net_model_path = "u2net.pth"
if not os.path.exists(u2net_model_path):
    st.error(f"U2Net model not found at {u2net_model_path}")
    st.stop()

from u2net import U2NET
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
u2net = U2NET(3,1)
u2net.load_state_dict(torch.load(u2net_model_path, map_location=device))
u2net.to(device)
u2net.eval()

def segment_person(image_path):
    image = Image.open(image_path).convert('RGB')
    transform = transforms.Compose([
        transforms.Resize((320,320)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
    ])
    img_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        d1, *_ = u2net(img_tensor)
        mask = d1[:,0,:,:]
        mask = (mask - mask.min()) / (mask.max() - mask.min() + 1e-8)
        mask = mask.squeeze().cpu().numpy()
        mask = cv2.resize(mask, (image.width, image.height))
        mask = (mask > 0.5).astype(np.uint8)

    img_np = np.array(image)
    img_np = img_np * mask[:,:,np.newaxis]
    segmented = Image.fromarray(img_np)
    return segmented

def predict_body_shape(image_path, model):
    """
    Predicts the body shape from an image using the loaded model.
    """
    # Use original image for prediction (NOT segmented)
    original_img = Image.open(image_path).convert("RGB")
    segmented_img = segment_person(image_path)  # only for visualization

    img_resized = original_img.resize((224,224))
    img_array = np.array(img_resized) / 255.0  # normalize
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    confidence = predictions[0][predicted_class_index]

    # Correct class label order
    class_labels = ['Apple','Hourglass','InvertedTriangle','Rectangle']

    return class_labels[predicted_class_index]

    # return class_labels.get(predicted_class_index, "Unknown")


# --- STREAMLIT UI ---
st.set_page_config(page_title="👗 StyleSense", layout="wide")
st.title("StyleSense: Your Body, Your Style, Our app")
st.markdown("Upload a full-body image of yourself and let our AI predict your body shape to give you personalized clothing recommendations.")

# Initialize session state variables
if 'predicted_body_shape' not in st.session_state:
    st.session_state.predicted_body_shape = None
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

# File uploader
uploaded_file = st.file_uploader("Choose a full-body image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # If a new file is uploaded, reset the prediction
    if uploaded_file != st.session_state.get("uploaded_file", None):
        st.session_state.uploaded_file = uploaded_file
        st.session_state.predicted_body_shape = None
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(uploaded_file.read())
            st.session_state.temp_path = tmp_file.name   # store in session_state

    # Always load temp_path from session_state
    temp_path = st.session_state.get("temp_path", None)

    if temp_path:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption='Uploaded Image', use_column_width=True)
        st.write("")

        if st.button("Predict Body Shape and Get Recommendations"):
            if model:
                with st.spinner('Analyzing your body shape...'):
                    predicted_shape = predict_body_shape(temp_path, model)
                    st.session_state.predicted_body_shape = predicted_shape
                st.success(f"Our AI has identified your body shape as: **{st.session_state.predicted_body_shape}**")
            else:
                st.error("The prediction model is not available. Please check the model file.")

# Check if a prediction has been made and is stored in session state
if st.session_state.predicted_body_shape:
    st.header(f"Recommendations for a {st.session_state.predicted_body_shape} Body Shape")
    
    st.markdown("---")
    st.subheader("Refine your recommendations")
    
    rules_for_filters = {
        "Rectangle": {
            "categories": ["Top", "Bottom", "Dress", "Outerwear"],
            "subcategories": ["Peplum Top", "Belted Shirt", "Ruffled Layered Top", "Flared Jeans", "A-line Skirt", "Pleated Skirt", "Wrap Dress", "Belted Dress", "Fit-and-Flare Dress", "Structured Blazer", "Waist Belt Jacket", "Cropped Blazer", "Saree", "Anarkali Suits", "Lehengas"],
            "fabrics": ["Cotton", "Linen", "Polyester", "Wool", "Denim"]
        },
        "Inverted Triangle": {
            "categories": ["Top", "Bottom", "Dress", "Outerwear"],
            "subcategories": ["V-Neck Top", "Scoop Neck Blouse", "Wrap Top", "Wide-leg Pants", "A-line Skirt", "Palazzo Pants", "Fit-and-Flare Dress", "A-Line Dress", "Bias-cut Dress", "Longline Jacket", "Waterfall Cardigan", "Slim Blazer", "Saree", "Kurtas and Tunics", "Anarkali Suits", "Lehengas"],
            "fabrics": ["Rayon", "Crepe", "Satin", "Georgette", "Silk Blend"]
        },
        "Hourglass": {
            "categories": ["Top", "Bottom", "Dress", "Outerwear"],
            "subcategories": ["Wrap Blouse", "Fitted Crop Top", "Structured Shirt", "High-waist Jeans", "Pencil Skirt", "Bodycon Skirt", "Bodycon Dress", "Sheath Dress", "Mermaid Gown", "Belted Trench Coat", "Cropped Jacket", "Fitted Blazer", "Saree", "Anarkali Suits", "Lehengas"],
            "fabrics": ["Spandex", "Denim", "Tweed", "Silk Blend", "Cotton"]
        },
        "Pear": {
            "categories": ["Top", "Bottom", "Dress", "Outerwear"],
            "subcategories": ["Off-Shoulder Top", "Boat Neck Blouse", "Puff Sleeve Shirt", "Straight-leg Pants", "Dark-colored Jeans", "A-line Skirt", "Empire Waist Dress", "A-line Dress", "Fit-and-Flare Dress", "Structured Shoulder Jacket", "Cropped Jacket", "Boxy Blazer", "Saree", "Anarkali Suits", "Lehengas"],
            "fabrics": ["Cotton", "Wool", "Denim", "Linen", "Organza"]
        },
        "Apple": {
            "categories": ["Top", "Bottom", "Dress", "Outerwear"],
            "subcategories": ["V-neck Blouse", "Flowy Wrap Top", "Longline Tunic", "Straight Pants", "Bootcut Pants", "High-waist Skirt", "Empire Waist Dress", "A-line Dress", "Wrap Dress", "Open-front Cardigan", "Longline Vest", "Blazer with Single Button", "Saree", "Kurtas and Tunics", "Anarkali Suits"],
            "fabrics": ["Chiffon", "Georgette", "Rayon", "Viscose", "Knit"]
        }
    }
    
    all_occasions = sorted(list(set(oc for p in products_data for oc in p['occasion'])))
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        dynamic_categories = rules_for_filters.get(st.session_state.predicted_body_shape, {}).get("categories", [])
        selected_categories = st.multiselect("Filter by Category:", dynamic_categories)
    
    with col2:
        dynamic_subcategories = rules_for_filters.get(st.session_state.predicted_body_shape, {}).get("subcategories", [])
        selected_subcategories = st.multiselect("Filter by Style (Subcategory):", dynamic_subcategories)
    
    with col3:
        dynamic_fabrics = rules_for_filters.get(st.session_state.predicted_body_shape, {}).get("fabrics", [])
        selected_fabrics = st.multiselect("Filter by Fabric:", dynamic_fabrics)
        
    with col4:
        selected_occasions = st.multiselect("Filter by Occasion:", all_occasions)
    
    st.markdown("---")
    
    # Get recommendations based on the stored body shape and current filters
    recommendations = get_recommendations_by_body_shape(
        products_data,
        st.session_state.predicted_body_shape,
        selected_fabrics,
        selected_occasions,
        selected_subcategories,
        selected_categories
    )
    
    if not recommendations:
        st.warning("Sorry, no items match your selection. Please adjust your filters.")
    else:
        st.subheader("Here are your personalized results:")
        num_columns = 3
        cols = st.columns(num_columns)
        col_index = 0
        
        for product in recommendations:
            with cols[col_index]:
                st.image(product["product_image"], use_column_width=True)
                st.markdown(f"**{product['product_subcategory']}**")
                st.markdown(f"Category: {product['product_category']}")
                st.markdown(f"Color: {product['color']}")
                st.markdown(f"Fabric: {product['fabric']}")
                st.markdown(f"Occasions: {', '.join(product['occasion'])}")
                
            col_index = (col_index + 1) % num_columns