const APP_ID = '03dd86e8444b4b8b98cd6b963c9b3a96'
const CHANNEL = 'main'
const TOKEN = '007eJxTYKir5zRxv6brOmXu1PTG996fTjGoTMk+qiqffKXcY0cYt4YCg4FxSoqFWaqFiYlJkkmSRZKlRXKKWZKlmXGyZZJxoqUZ48eFyQ2BjAy6XRMZGRkgEMRnYchNzMxjYAAAuuAdeA=='
let UID;

const client = AgoraRTC.create_client({mode:'rtc', codec:'vp8'})

let localTracks = []
let remoteUsers = {}

let joinAndDisplayLocalStream = async() => {
    UID = await client.join(APP_ID, CHANNEL, TOKEN, null)

    localTracks await AgoraRTC.createMicrophoneAndCameraTracks()
    let player = `<div class="video-container" id="user-container-${UID}">
                    <div class="video-player" id="user-${UID}"></div>
                    <div class="username-wrapper"><span class="user-name">My Name</span></div>
                </div>`
    
    document.getElementById("video-streams").insertAdjacentHTML('beforeend',player)
    
    localTracks[1].play(`user-${UID}`)

    await client.publish([localTracks[0],localTracks[1]])


}

joinAndDisplayLocalStream()


