# Test Document

This document is used to test the preprocessor.

| Content Type | Schema    |
|--------------|-----------|
| test-ref     | test.json |
| missing-ref  | BAD.json  |

# My Endpoint [/end/]

## Come get some [GET]

+ Response (test-ref)

  + Headers

    ```
    Link: </test.json>; rel="describedBy"
    ```

  + Body

    ```js
    {}
    ```

  + Schema

    ```js
    {
      "random": "This gets replaced"
    }
    ```

+ Request (missing-ref)

  + Body

    ```js
    {}
    ```

  + Schema

    ```js
    {"ignore": "this should still be here since the json file doesn't exist"}
    ```

+ Request (other-ref)

  + Body

    ```js
    {}
    ```

  + Schema

    ```js
    {"ignore": "this should still be here since there isn't a matching ref"}
    ```

+ Request (test-ref)

  + Body

    ```js
    {}
    ```

This block still has a content type set, since there wasn't a schema in the above block.

+ Request

  We no longer have a content type.

  + Schema

    ```js
    {"this will not be replaced": "since we entered a new block without a content type"}
    ```

This request will get the schema replaced.

+ Request (test-ref)

  + Headers

    ```
    Link: </test.json>; rel="describedBy"
    ```

  + Body

    ```js
    {}
    ```

  + Schema

    ```js
    {
      "random": "This gets replaced"
    }
    ```

