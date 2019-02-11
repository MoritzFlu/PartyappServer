# PartyappServer
Server für SWENG Partyapp


Grobe Struktur:

    Komponenten:   

        ClientHandler/TCPServer
            Stellt Verbindungen zu Clients her, ruft andere Komponenten auf
            Handelt die von CLients empfangenen Daten

        PointHandler 
            Modus Zeit oder Events, Verteilet Punkte an User
            Startet Events oder verteilt nach Ablauf eines Timers

        MusicHandler
            Interagiert mit der Lieder DB und den Playlists
            Bitet Funktionen daten anzuzeigen oder playlists zu ändern
            enthält selbst keine wirkliche Entscheidungslogik

        MusicDB
            Enthält DB aller Localer Lieder oder wird durch Spotify Ersetzt

        ServerDB
            Enthält Playlist, UserDaten, ...
            
