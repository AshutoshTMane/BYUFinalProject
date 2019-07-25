import wsgiref.simple_server
import urllib.parse
import sqlite3
import http.cookies


connection = sqlite3.connect('players.db')
stmt = "SELECT name FROM sqlite_master WHERE type='table' AND name='players'"
cursor = connection.cursor()
result = cursor.execute(stmt)
r = result.fetchall()
if not r:
    exp = 'CREATE TABLE players (FirstName, SecondName)'
    connection.execute(exp)

def application(environ, start_response):
    headers = [('Content-Type', 'text/html; charset=utf-8')]

    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    n1 = params['FirstName'][0] if 'FirstName' in params else None
    n2 = params['SecondName'][0] if 'SecondName' in params else None
    print(n1)
    if path == '/':
        print('hello')

        page = '''<!DOCTYPE html>
        <html><head><title>Player Names</title></head><body>
        <h1 style="color: black">Sonar Treasure Hunt!</h1>
        <h2 style="background-color: white">A 2-player co-op game</h2>
        <p>Please enter your names before we head to sea!</p>
        <form action="/game" style="background-color:white">
            Player 1 Name: <input type="text" name="FirstName"><br>
            Player 2 Name: <input type="text" name="SecondName"><br>
            <input type="submit" value="To Sea!">
        </form>
        <p><a href="/tutorial">Tutorial</a></p>
        </body>
        </html>'''
        return [page.encode()]

    if path == '/game' and n1 and n2:
        players = cursor.execute('SELECT * FROM players WHERE FirstName = ? AND SecondName = ?', [n1, n2]).fetchall()
        if players:
            print(n1)
            print(n2)
            headers.append(('Set-Cookie', 'session={}:{}'.format(n1, n2)))
            start_response('200 OK', headers)
            return ['''Welcome Captain {}! Welcome Co-Captain {}!'''.format(n1, n2).encode()]
        else:
            connection.execute('INSERT INTO players VALUES (?, ?)', [n1, n2])
            connection.commit()
            headers.append(('Set-Cookie', 'session={}:{}'.format(n1, n2)))
            start_response('200 OK', headers)
            return ['''Welcome Captain {}! Welcome Co-Captain {}!'''.format(n1, n2).encode()]

    if path == '/tutorial':
        page = '''<!DOCTYPE html>
                <html><head><title>Sonar Tutorial</title></head><body>
                <h1 style="color: black">Instructions:</h1>
<p>You are the captain of the Simon, a treasure-hunting ship.</p>
<p>Your current mission
is to use sonar devices to find three sunken treasure chests at the bottom of
the ocean.</p>
<p>But you only have cheap sonar that finds distance, not direction.</p>
<p>Enter the coordinates to drop a sonar device.</p>
<p>The ocean map will be marked with
how far away the nearest chest is, or an X if it is beyond the sonar device's
range.</p>
<p>For example, the C marks are where chests are.</p>
<p>The sonar device shows a 3 because the closest chest is 3 spaces away.</p>
<p></p>
<p>012345678901234567890123456789012</p>
<p>0 ~~~~`~```~`~``~~~``~`~~``~~~``~`~ 0</p>
<p>1 ~`~`~``~~`~```~~~```~~`~`~~~`~~~~ 1</p>
<p>2 `~`C``3`~~~~`C`~~~~`````~~``~~~`` 2</p>
<p>3 ````````~~~`````~~~`~`````~`~``~` 3</p>
<p>4 ~`~~~~`~~`~~`C`~``~~`~~~`~```~``~ 4</p>
<p>012345678901234567890123456789012</p>
<p></p>
<p>(In the real game, the chests are not visible in the ocean.)</p>
<p>When you drop a sonar device directly on a chest, you retrieve it and the other
sonar devices update to show how far away the next nearest chest is.</p>
<p>The chests
are beyond the range of the sonar device on the left, so it shows an X.</p>
<p></p>
<p>012345678901234567890123456789012</p>
<p>0 ~~~~`~```~`~``~~~``~`~~``~~~``~`~ 0</p>
<p>1 ~`~`~``~~`~```~~~```~~`~`~~~`~~~~ 1</p>
<p>2 `~`X``7`~~~~`C`~~~~`````~~``~~~`` 2</p>
<p>3 ````````~~~`````~~~`~`````~`~``~` 3</p>
<p>4 ~`~~~~`~~`~~`C`~``~~`~~~`~```~``~ 4</p>
<p>012345678901234567890123456789012</p>
<p></p>
<p>The treasure chests don't move around.</p>
<p>Sonar devices can detect treasure chests
up to a distance of 9 spaces.</p>
<p>Try to collect all 3 chests before running out of
sonar devices.</p>
<p>Good luck!</p>
        <p><a href="/">Back</a></p>
        <br />
                </html>'''
        return [page.encode()]

httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()