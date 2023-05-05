import { useState } from "react";
import Title from "./Title";
import RecordMessage from "./RecordMessage";
import axios from "axios";

function Controller() {
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);

  const createBlobUrl = (data: any) => {
    const blob = new Blob([data], { type: "audio/mpeg" });
    return window.URL.createObjectURL(blob);
  };

  const handleStop = async (blobUrl: string) => {
    setIsLoading(true);

    // Append recorded message to messages
    const myMessage = { sender: "me", blobUrl };
    const messagesArr = [...messages, myMessage];

    // convert blob url to blob object
    await fetch(blobUrl)
      .then((res) => res.blob())
      .then(async (blob) => {
        // construct audio to send file
        const formData = new FormData();
        formData.append("file", blob, "myFile.wav");

        //send form data to API endpoint
        await axios
          .post("http://127.0.01:8000/post-audio", formData, {
            headers: { "Content-Type": "audio/mpeg" },
            responseType: "arraybuffer",
          })
          .then((res: any) => {
            const blob = res.data;
            const audio = new Audio();
            audio.src = createBlobUrl(blob);

            //Append to audio
            const rachelMessage = { sender: "rachel", blobUrl: audio.src };
            messagesArr.push(rachelMessage);
            setMessages(messagesArr);

            //play audio
            setIsLoading(false);
            audio.play();
          })
          .catch((err: any) => {
            console.error(err.message);
            setIsLoading(false);
          });
      });
  };

  return (
    <div className="h-screen overflow-y-hidden">
      <Title setMessages={setMessages} />
      <div className="flex flex-col justify-between h-full overflow-y-scroll pb-96">
        {/*conversation*/}
        <div className="mt-5 px-5">
          {messages.map((audio, index) => {
            return (
              <div
                key={index + audio.sender}
                className={
                  "flex flex-col " +
                  (audio.sender === "rachel" && "flex items-end")
                }
              >
                {/*sender*/}
                <div className="mt-4">
                  <p
                    className={
                      audio.sender === "rachel"
                        ? "text-right font-bold py-1 mr-2 italic text-green-500"
                        : "text-left ml-2 font-bold py-1 italic text-blue-500"
                    }
                  >
                    {audio.sender}
                  </p>

                  {/* Audio Message */}
                  <audio
                    src={audio.blobUrl}
                    className="appearance-none"
                    controls
                  />
                </div>
              </div>
            );
          })}
          {messages.length === 0 && !isLoading && (
            <div className="text-center text-2xl font-light italic mt-10">
              Send Rachel a message...
            </div>
          )}
          {isLoading && (
            <div className="text-center font-light italic mt-10 animate-pulse">
              Gimme a few seconds...
            </div>
          )}
        </div>
        <div className="fixed bottom-0 w-full py-6 text-center border-t bg-gradient-to-r from-sky-500 to-green-500">
          <div className="flex place-content-center w-full">
            <RecordMessage handleStop={handleStop} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Controller;
