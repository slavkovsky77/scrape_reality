yit_apartments_payload = {
    "PageSize": 0,
    "StartPage": 0,
    "QueryString": "*",
    "UILanguage": "en",
    "PageId": 21747,
    "BlockId": 0,
    "SiteId": "yit.sk",
    "Attrs": [
      "inap"
    ],
    "Fields": None,
    "CacheMaxAge": 300,
    "Filter": {
      "Field": "Locale",
      "Value": "en",
      "Operator": "Equals",
      "AndConditions": [
        {
          "Field": "ProjectPublish",
          "Value": True,
          "Operator": "Equals",
          "AndConditions": [],
          "OrConditions": []
        },
        {
          "Field": "IsAvailable",
          "Value": True,
          "Operator": "Equals",
          "AndConditions": [],
          "OrConditions": []
        },
        {
          "Field": "ProductItemForSale",
          "Value": True,
          "Operator": "Equals",
          "AndConditions": [],
          "OrConditions": []
        },
        {
          "Field": "AreaIds",
          "Value": "cityv62u-q27j-49ue-j59q86mus34t",
          "Operator": "Any",
          "AndConditions": [],
          "OrConditions": []
        },
        {
          "Field": "BuildingTypeKey",
          "Value": [
            "BlockOfFlats",
            "SemiDetachedHouse",
            "DetachedHouse"
          ],
          "Operator": "In",
          "AndConditions": [],
          "OrConditions": []
        }
      ],
      "OrConditions": []
    },
    "Facet": [
      {
        "Field": "ApartmentSize",
        "Operator": "GreaterOrEqual",
        "Interval": 10
      },
      {
        "Field": "ApartmentSize",
        "Operator": "LessOrEqual",
        "Interval": 10
      },
      {
        "Field": "SalesPrice",
        "Operator": "GreaterOrEqual",
        "Interval": 10000
      },
      {
        "Field": "SalesPrice",
        "Operator": "LessOrEqual",
        "Interval": 10000
      }
    ]
  }