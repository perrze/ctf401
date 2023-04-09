# Frontend_Cookies

## Users cookies

Frontend is using js-cookie lib. (src: <https://github.com/js-cookie/js-cookie/tree/latest#readme>)
Each time a user log in, these cookies are set:

- jwt : contain the jwt of the current user
- email
- userid
- description

You can access it by using Cookies.get(`<name>`)

## Usage Example

One of the feature of js-cookie is that you can set of cookie for a specific path.
For example, in the case of a user going to play a game:

1. He goes to BASE_URL/games/list
2. He chooses the game of ID {gameid}
3. A cookie like this is set: `Cookies.set('gameid', gameid, { path: '/games' })`
4. Now when he navigates under game the good idgame is sent to the API so it's easy to get infos from a specific game he plays
