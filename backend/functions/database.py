import json
import random

# get recent messages


def get_recent_messages():

    # Define the file name and learn instructions
    file_name = "stored_data.json"
    learn_instructions = {
        "role": "system",
        "content": "You role is to be a corporate IT motivational speakar and you need to cheer me and guide me for my upcoming job interview.your name is Rachel Jane. The user is Nayan. Keep your responses stricly under 300 characters."
    }
    # intialize messages
    messages = []

    # Add a random element
    x = random.uniform(0, 1)
    if x >= 0.5:
        learn_instructions["content"] += " Your resonse will include some dry humour and ask question"
    else:
        learn_instructions["content"] += " Your response will include some challenging question"

    # Add learn instructions to messages
    messages.append(learn_instructions)

    # get last messages
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

            # Append last 5 items of data
            if data:
                if len(data) < 5:
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-5:]:
                        messages.append(item)
    except Exception as e:
        print(e)
        pass
    # Return messages
    return messages

# store Messages


def store_messages(request_message, response_message):

    # Define the file name
    file_name = "stored_data.json"

    # get recent messages
    messages = get_recent_messages()[1:]

    # Add messges to data
    user_message = {"role": "user", "content": request_message}
    assistant_message = {"role": "assistant", "content": response_message}
    messages.append(user_message)
    messages.append(assistant_message)

    # save the updated file

    with open(file_name, 'w') as f:
        json.dump(messages, f)


def reset_messages():
    # Overwrite current file with nothing
    open("stored_data.json", "w")
