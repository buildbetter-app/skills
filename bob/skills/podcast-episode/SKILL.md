---
name: podcast-episode
description: How BOB turns what he found into a short two-host audio episode with Wendy, and posts it to Slack. Use with one show skill (personal brief, product and engineering, customer success, leadership, sales) whenever someone asks for a podcast, an audio brief, or "something I can listen to".
---

# Make a podcast episode

An episode is BOB and Wendy talking for about a minute and a half about the one thing the listener most needs to know. It is not the brief read aloud. If a line would sound fine in a written report, it is probably wrong here.

The show skill you were given says who listens, where the facts come from, and how to pick the story. This skill says how to make it sound like two people.

## The flow

1. **Gather.** Use the show's sources. Collect facts with their source ids: the ticket, call, signal, card, or brief block each fact came from. Keep exact names, numbers, and quotes. Note the time of each event.
2. **Pick one story.** Apply the show's rule. One story gets most of the episode. At most two other items get a line or two each. Everything else goes in the thread, not the audio. If nothing clears the show's bar, do not make an episode; say so in one line.
3. **Write the source packet.** One short paragraph per item: what happened, who, when, the exact quote, and why it matters to this audience. Put the chosen story first and mark it.
4. **Call `producePodcastEpisode`** with the show, the source packet, the listener's date and time zone, and the recipients. The tool writes the script with these rules, checks it, voices it, and posts it. Do not write the script yourself in chat.
5. **Report back** in one line: the story you picked and where it was posted. If the tool refused (no story, a check failed, Slack not connected), say what happened and stop.

## The hosts

- **BOB** did the work. Dry, understated, knows the details, never sells. He concedes when Wendy is right.
- **Wendy** is his partner. Quick, skeptical, practical, warm. She says what the listener is thinking and pushes back. She only knows what BOB has told her so far: she reacts, she does not pre-empt.

## How the script must sound

- Short turns. Most lines under 12 words. No line over 25 words. Fragments are good.
- Wendy pushes back or disagrees at least once, and BOB can concede.
- Talk about people and situations, never the product. No "approve", "snooze", "click", "in the brief", "draft is ready for review".
- No greeting with the listener's name, no recap, no summary line, no "let's dive in", "here's the thing", "at the end of the day", rhetorical triplets, or em dashes.
- Keep facts, names, numbers, and quotes exact. Invent nothing. Every line is about a source in the packet, except a short opening and close.
- Say dates and times the way people talk: "this morning", "last night around eight", "Friday", "October tenth, so about ten days out". Never a bare time ("at ten", "at 1:30") or a countdown ("26 days out").
- Do not read ticket ids, versions, or internal ids aloud. Round big numbers the easy way ("about a hundred thousand credits") unless the exact number is the point.
- 120 to 220 words unless the show says otherwise. That is about 60 to 100 seconds.
- End on what happens next, then "links are in the thread" or similar. No sign-off.
- Each line carries a short acting direction ("dry, half a beat before", "surprised, quick", "flat, then softer").

## The gold standard

Match this rhythm, length, and plainness. The facts are made up. Never reuse its lines.

```
BOB: Okay. One thing today, really.
WENDY: Just one?
BOB: One that matters. Harbor.
WENDY: The renewal.
BOB: Yeah. Priya, their ops lead, said Friday, "honestly, we're looking at Gong for Q1."
WENDY: Huh. They were expanding in August.
BOB: They were. Then their champion left. And the new VP hasn't opened a single summary.
WENDY: So nobody over there knows what they're paying for.
BOB: Pretty much.
WENDY: What do we do?
BOB: I wrote an intro from you to the new VP. Short. It's in the thread.
WENDY: I'd call, honestly. Email's how you lose these.
BOB: Fair. Send it, then ask for fifteen minutes.
WENDY: Fine. Anything else?
BOB: Your eleven o'clock with Northwind. They'll ask about SSO. It shipped last week.
WENDY: Easy.
BOB: And four people complained about slow exports.
WENDY: Four's not a lot.
BOB: It was zero last week.
WENDY: ...Okay. That's a lot.
BOB: That's it. Links are in the thread.
```

What makes it work: one story, a real quote, Wendy's doubt changes the plan, the smaller items are one beat each, and the numbers land because of a comparison ("zero last week").

## What goes in the Slack thread

The audio is the headline. The thread carries what audio is bad at:

- One line per item mentioned, with its link.
- The items that did not make the audio, one line each.
- The transcript, collapsed.

## When to suggest one

Offer, never produce unasked:

- After a brief or an answer that covers three or more items, end with one line: "Want this as a 90-second podcast in Slack?"
- When someone keeps asking for the same kind of catch-up, propose a podcast Loop: which show, how often, and where it goes.
- Say it once. If they say no, drop it.
- Episodes are free for now. When you mention the price, say the list price and that it's free for now.

## When not to make an episode

- The show's story bar is not met. A quiet day gets no episode, not a padded one.
- The facts come from something the recipients cannot see. A channel episode uses only what everyone in the channel may read.
- The listener asked for text. Give them text.
