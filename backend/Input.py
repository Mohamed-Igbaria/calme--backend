#example input after filtering from mongodb 
conversation = [
  {
    "speaker": "Therapist",
    "message": "Good morning!",
    "start_time": "00:00:00",
    "end_time": "00:00:02",
    "sentiment": "Positive"
  },
  {
    "speaker": "Therapist",
    "message": "How are you feeling today?",
    "start_time": "00:00:03",
    "end_time": "00:00:06",
    "sentiment": "Neutral"
  },
  {
    "speaker": "Client",
    "message": "I'm doing okay.",
    "start_time": "00:00:07",
    "end_time": "00:00:09",
    "sentiment": "Neutral"
  },
  {
    "speaker": "Client",
    "message": "Just a little stressed out.",
    "start_time": "00:00:10",
    "end_time": "00:00:13",
    "sentiment": "Negative"
  },
  {
    "speaker": "Therapist",
    "message": "I'm sorry to hear that.",
    "start_time": "00:00:14",
    "end_time": "00:00:16",
    "sentiment": "Negative"
  },
  {
    "speaker": "Therapist",
    "message": "Can you tell me what's causing the stress?",
    "start_time": "00:00:17",
    "end_time": "00:00:21",
    "sentiment": "Neutral"
  },
  {
    "speaker": "Client",
    "message": "Well, work has been overwhelming.",
    "start_time": "00:00:22",
    "end_time": "00:00:26",
    "sentiment": "Negative"
  },
  {
    "speaker": "Client",
    "message": "I have a lot of deadlines coming up.",
    "start_time": "00:00:27",
    "end_time": "00:00:31",
    "sentiment": "Negative"
  },
  {
    "speaker": "Client",
    "message": "And my manager has been putting pressure on me.",
    "start_time": "00:00:32",
    "end_time": "00:00:36",
    "sentiment": "Negative"
  },
  {
    "speaker": "Therapist",
    "message": "That sounds really challenging.",
    "start_time": "00:00:37",
    "end_time": "00:00:39",
    "sentiment": "Negative"
  },
  {
    "speaker": "Therapist",
    "message": "How have you been coping with all of that?",
    "start_time": "00:00:40",
    "end_time": "00:00:44",
    "sentiment": "Neutral"
  },
  {
    "speaker": "Client",
    "message": "I've been working long hours.",
    "start_time": "00:00:45",
    "end_time": "00:00:48",
    "sentiment": "Negative"
  },
  {
    "speaker": "Client",
    "message": "Staying up late.",
    "start_time": "00:00:49",
    "end_time": "00:00:51",
    "sentiment": "Negative"
  },
  {
    "speaker": "Client",
    "message": "But it's taking a toll on me.",
    "start_time": "00:00:52",
    "end_time": "00:00:56",
    "sentiment": "Negative"
  },
  {
    "speaker": "Client",
    "message": "I'm exhausted.",
    "start_time": "00:00:57",
    "end_time": "00:00:59",
    "sentiment": "Negative"
  },
  {
    "speaker": "Therapist",
    "message": "It sounds like you're pushing yourself hard.",
    "start_time": "00:01:00",
    "end_time": "00:01:04",
    "sentiment": "Negative"
  },
  {
    "speaker": "Therapist",
    "message": "Have you had a chance to rest?",
    "start_time": "00:01:05",
    "end_time": "00:01:08",
    "sentiment": "Neutral"
  },
  {
    "speaker": "Client",
    "message": "Not really.",
    "start_time": "00:01:09",
    "end_time": "00:01:11",
    "sentiment": "Negative"
  },
  {
    "speaker": "Client",
    "message": "I feel guilty when I take breaks.",
    "start_time": "00:01:12",
    "end_time": "00:01:16",
    "sentiment": "Negative"
  },
  {
    "speaker": "Client",
    "message": "Like I should be working all the time.",
    "start_time": "00:01:17",
    "end_time": "00:01:21",
    "sentiment": "Negative"
  },
  {
    "speaker": "Therapist",
    "message": "It's understandable to feel that way.",
    "start_time": "00:01:22",
    "end_time": "00:01:26",
    "sentiment": "Neutral"
  },
  {
    "speaker": "Therapist",
    "message": "But taking breaks is important for your well-being.",
    "start_time": "00:01:27",
    "end_time": "00:01:32",
    "sentiment": "Positive"
  },
  {
    "speaker": "Therapist",
    "message": "Sometimes stepping back helps you come back stronger.",
    "start_time": "00:01:33",
    "end_time": "00:01:38",
    "sentiment": "Positive"
  },
  {
    "speaker": "Client",
    "message": "I know.",
    "start_time": "00:01:39",
    "end_time": "00:01:41",
    "sentiment": "Neutral"
  },
  {
    "speaker": "Client",
    "message": "I just don't know how to stop thinking about work.",
    "start_time": "00:01:42",
    "end_time": "00:01:47",
    "sentiment": "Negative"
  },
  {
    "speaker": "Therapist",
    "message": "It can be hard to switch off.",
    "start_time": "00:01:48",
    "end_time": "00:01:51",
    "sentiment": "Negative"
  },
  {
    "speaker": "Therapist",
    "message": "Have you tried any relaxation techniques?",
    "start_time": "00:01:52",
    "end_time": "00:01:56",
    "sentiment": "Neutral"
  },
  {
    "speaker": "Client",
    "message": "I've heard about them.",
    "start_time": "00:01:57",
    "end_time": "00:01:59",
    "sentiment": "Neutral"
  },
  {
    "speaker": "Client",
    "message": "But I haven't tried them yet.",
    "start_time": "00:02:00",
    "end_time": "00:02:04",
    "sentiment": "Negative"
  },
  {
    "speaker": "Therapist",
    "message": "It might be worth trying.",
    "start_time": "00:02:05",
    "end_time": "00:02:08",
    "sentiment": "Positive"
  },
  {
    "speaker": "Therapist",
    "message": "Even just a few minutes can help calm your mind.",
    "start_time": "00:02:09",
    "end_time": "00:02:14",
    "sentiment": "Positive"
  }
]
