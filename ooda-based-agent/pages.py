PAGES = {
    1: {
        "text": "The 20-mph (32 kph) speed limit makes it easy to read the doors as you drive your Ford Escort east on Prince of Wales Road. The house numbers count down along a mishmash of terraces, interrupted only by the pillared front of a former Methodist chapel, now a contemporary art centre with the obligatory cafe and gift shop. You find what you're looking for in the low hundreds and, by some miracle, there is a parking space opposite, just wide enough for your car. Safely wedged into the parking space, you take a moment to review the report. Verbal disagreements in the basement flat, three nights in a row. Two voices heard, getting louder each time. Culminating on the third night in an almighty crash that prompted a 999 (emergency services) call from the couple upstairs, the Romanian students next door, and a cyclist delivering curry who was startled enough to drop his bag over the railing, ending up with an unholy amalgam of tikka masala, korma, and saag aloo. The responding officers found signs of a struggle, but no other persons on the premises. You step from the car to see an unsympathetic-looking woman wearing a Hi-Viz safety jacket, a peaked cap, and an acid perm. She is a Civil Enforcement Officer, otherwise known as a parking warden. She notes down your car's registration number.",
        "choices": [{"text": "Se você é um Policial (Police Officer)", "goto": 9}, {"text": "Se você é um Assistente Social (Social Worker)", "goto": 42}, {"text": "Se você é um Enfermeiro (Nurse)", "goto": 72}]
    },
    2: {
        "text": "The rush hour traffic begins to break as you chauffeur Ernie across Euston Road and back north. Somewhere near Mornington Crescent he starts snoring. You stop around the corner from Prince of Wales Road to pick up supplies. On your third circuit, a parking space opens up in front of Mrs Fellaman's flat and you cut up an aggrieved woman in a Chelsea tractor to secure the spot. It is seven o'clock. Around eight, Ernie stirs. You watch him closely, but the way he whines and paws the door suggests no magic is involved. He lets you attach the lead and take him down a cul-de-sac for a comfort break. You capture the results in a latex glove and dispose of them lawfully. Ernie is willing to return to the car, which has remarkably not been ticketed during your three-minute absence. He shows no particular interest in Mrs Fellaman's flat and nods off again. You settle in to continue the stakeout. Characters recover over time. If you were Hurt, you now return to normal; update your character sheet by erasing the \"Hurt\" mark.",
        "choices": [{
            "goto": 7,
            "effects": [{"action": "heal_damage", "amount": 4}]
        }]
    },
    3: {
        "text": "You hear the scuff of feet behind the door. It then opens and a little old woman sticks her head around the doorjamb. \"Yes? Can I help you?\" You ask if she is Mrs Eugenia Fellaman. \"Yes.\" Her eyes narrow. \"Are you with those two boys from earlier?\" You assure Mrs Fellaman you have come alone. She opens the door and steps out, blinking. As she steps up and scans the street, you notice the faded purple of a bruise on her left cheek.",
        "choices": [{"text": "Perguntar diretamente sobre o hematoma", "goto": 14}, {"text": "Esperar que ela retorne para a porta", "goto": 20}, {"text": "Aproveitar a oportunidade para olhar dentro da casa", "goto": 31}, {"text": "Perguntar sobre 'aqueles dois rapazes'", "goto": 35}, {"text": "Insistir para entrar e conversar", "goto": 46}]
    },
    4: {
        "text": "Wild-eyed, Knuckles grits his teeth as he swings the heavy masonry hammer at you. Knuckles is initiating an attack against you. His \"action\" is to try to hit you with his hammer. His Fighting skill is 40/20 (which means Regular 40/Hard 20). As the target of his attack, you get to \"respond.\" You may use a combat manoeuvre-a special type of attack to break his grip on the hammer. Decide whether you want to disarm your opponent or flee. Then carry out an opposed Fighting roll: Knuckles makes a Fighting roll and gets a Regular success. Make your own Fighting roll and compare the result to Knuckle's Regular success. Remember, a dice result of triple zero (100) is a fumble, while a 01 is a Critical success.",
        "choices": [{
            "opposed_roll": "Fighting",
            "opponent_skill": {"full": 40, "half": 20},
            "outcomes": {
                "win": {"goto": 8},
                "lose": {"goto": 12, "effects": [{"action": "take_damage", "amount": 2}]},
                "draw": {"goto": 28}
            }
        }]
    },
    5: {
        "text": "You pull out of your precious parking space and turn south towards Russell Square, taking Camden Street to avoid the shuffling mass of tourists attracted to the Lock by overpriced hummus wraps, Doc Martens, and spicy noodles. On the edge of Somers Town you see a local butcher and pop out of the car for a necessary purchase. The Folly occupies a Georgian terrace on the south side of Russell Square, a location it shares with the Council of British International Schools, the London Mathematical Society, and a birdshit-covered statue of the fifth Duke of Bedford. You pull into the garage around the back. DC Grant's Ford Focus ST, or \"Asbo,\" is not there a bad sign. But perhaps his dog Toby is still in residence. Inside the Folly, Toby's basket is empty. A familiar ink-skirted figure glides past, her gaze moving across you like a duster on a long-neglected shelf. This is the housekeeper, Molly. You work up some courage and ask her if you can borrow the Folly's famed ghost-hunting dog. She stops and tilts her head to the side, the black almond-shaped eyes beneath her mob cap skewering you where you stand. After an awkward silence, you repeat the request, holding up your sausages. For a moment the meaty packet sits in your hand like a terrible, inadvertent insult. Then Molly straightens her head and glides to the door. She points to the far corner of the yard in a manner reminiscent of Donald Sutherland at the end of Invasion of the Body Snatchers.",
        "choices": [{"goto": 11}]
    },
    6: {
        "text": "A masonry hammer pushes the glass inwards. Spiky fragments fall to the floor among the crockery. The heavy metal head runs around the frame, clearing the remaining spikes before its wielder steps through. He is a square and yobbish twentysomething with a bent nose, tattooed knuckles, and cold eyes. \"I told you there'd be consequences, Genie. You can't just borrow money and not pay it back.\" Knuckles notices the crockery on the floor. \"Strewth. Some other mob get here before us?\" A second man steps through the window, with a flat cap, a bad goatee, and a missing incisor. He points at you. \"Who's this?\" \"A witness,\" Knuckles says. He hefts the hammer and steps towards you. His body language says he is looking for a chance to use it. \"Beat it,\" he snarls.",
        "choices": [{"text": "Se você é um Policial, identifique-se", "goto": 19}, {"text": "Lançar feitiço Impello", "goto": 26}, {"text": "Lançar feitiço Scindere", "goto": 69}, {"text": "Enfrentar o agressor fisicamente", "goto": 4}]
    },
    7: {
        "text": "A little after nine o'clock the parking warden emerges from the darkness, light from the streetlamps glinting on her Hi-Viz jacket. She takes a momentary interest in the Escort, but seeing you behind the wheel, she rolls her eyes and moves on. Ernie growls from the back seat. Although resentment of traffic wardens could be his natural inclination, you turn around to calm your borrowed dog. He is not reacting to the traffic warden. His ears are forward, his tail straight back. He stares at the building, his attention completely focused on the basement flat, and barks twice. This is as good a confirmation of supernatural activity as you will get, and judging from the witness reports, indicates the presence of a ghost. You slip out of the Escort and shut Ernie inside. From the pavement, you can hear an argument. A raised voice, Mrs Fellaman's, and then a response-a younger, deeper, male voice. It is followed by the crash of breaking crockery.",
        "choices": [{"text": "Bater firmemente na porta", "goto": 13}, {"text": "Deslizar para os fundos", "goto": 33}, {"text": "Atrair a Sra. Fellaman para fora batendo na janela e se escondendo", "goto": 70}]
    },
    8: {
        "text": "You step inside the hammer's swing, closing to an intimate distance and negating Knuckles' advantage.",
        "choices": [{"text": "Se decidiu desarmar seu oponente", "goto": 23}, {"text": "Se decidiu fugir da luta", "goto": 109}]
    },
    9: {
        "text": "You show your warrant card to the parking warden. She grimaces. It's understandable, working as she does for the Parking Operations Operations Team (POOT), formerly the Parking Services Operations Team (before that, it was the Parking Services Enforcement Team). She eyes your plainclothes and the Ford Escort. \"Are you on official business?\" she asks, stylus poised above her battered handheld computer, desperately holding onto the fraying threads of her authority.",
        "choices": [{"goto": 17}]
    },
    10: {
        "text": "Mrs Fellaman heads for the kitchen. You take a moment to survey the flat. Ignoring a chair with its legs broken and the fragments of crockery strewn across the floor, you can see the Victorian origins of the building this flat was previously the servants' quarters, as well as the kitchen and coal bunker. Everything is crammed into a tight space with a low ceiling. The fireplace is bricked up. You have a moment to consider how to handle the ghost in this place. A magical intervention will be required. Spells in ROL:RPG are cast by forming shapes in the mind (forma). First order spells use only a single forma. DCI Nightingale, the Folly's resident master of magic, has taught you lux, which you used to master the spell Werelight. You have not yet practised enough to learn a second order spell combining two forma. But you have learned a second forma and can use it for another first order spell.",
        "choices": [{"text": "Se decidiu aprender Impello", "goto": 21}, {"text": "Se decidiu aprender Scindere", "goto": 30}]
    },
    11: {
        "text": "From the corner of the yard, behind the bins, comes the sound of bestial rage and mortal combat. Something in the shadows tears through plastic and cardboard, snarling through its teeth. It does not sound much like Toby the Ghost-Hunting Dog, who has a generally amiable personality, with a distinct affinity for anybody providing food.",
        "choices": [{"text": "Aproximar-se sorrateiramente das lixeiras para olhar", "goto": 15}, {"text": "Continuar a vigilância à distância", "goto": 24}]
    },
    12: {
        "text": "You try to step back from the swing, but the heavy hammer smashes into your shoulder and knocks you off-balance. Mark down that you take 2 damage. If you have suffered 2 damage in total, you are Bloodied, and so mark the Hurt and Bloodied boxes on your character sheet and go to 34. If you have suffered a total of 3 or more damage, you are Down, and so mark the Down box on your character sheet and go to 78.",
        "effect": {"damage_taken": 2},
        "choices": [{"text": "Se o total de dano for 2", "goto": 34}, {"text": "Se o total de dano for 3 ou mais", "goto": 78}]
    },
    13: {
        "text": "You descend the iron stairs. As you hear another plate shatter, you rap on the door. Immediately all noise ceases from inside. Nothing moves for 30 seconds. You lift up the letterbox and yell to Mrs Fellaman that you know she's in there and you don't intend to leave. After a prolonged pause, you hear the scuff of reluctant feet, and the door opens once more. Anger and guilt battle on Mrs Fellaman's face. \"What do you want this time?\" she says.",
        "choices": [
            {
                "conditional_on": "occupation",
                "paths": {
                    "Police Officer": {
                        "text": "Usar sua autoridade como Policial",
                        "goto": 18
                    },
                    "default": {
                        "text": "Tentar usar sua força de vontade (não-policial)",
                        "roll": "POW",
                        "results": {
                            "2": {"goto": 27},
                            "3": {"goto": 22}
                        }
                    }
                }
            }
        ]
    },
    14: {
        "text": "Mrs Fellaman stops as you ask about the bruise. She very deliberately does not lift her hand to her cheek. \"I walked into the door, didn't I?\" she says. \"You get like that when you're a bit older.\" You find a gentle way to say that neither of you believes that. She screws up her nose and pushes past you, back into the doorway.",
        "choices": [{"text": "Esperar pacientemente que a Sra. Fellaman o convide para entrar", "goto": 61}, {"text": "Procurar por algo que possa facilitar uma entrada ilícita", "goto": 71}, {"text": "Perguntar sobre os 'dois rapazes'", "goto": 76}, {"text": "Insistir em olhar dentro da casa", "goto": 82}]
    },
    15: {
        "text": "The volume of the snarling and rending increases as you pad across the yard and press yourself against the wall to look behind the bins. Abruptly, the noise stops. Make a Stealth roll.",
        "choices": [{
            "roll": "Stealth",
            "results": {
                "5": {"goto": 29},
                "4": {"goto": 29},
                "3": {"goto": 29},
                "2": {"goto": 40},
                "1": {"goto": 40}
            }
        }]
    },
    16: {
        "text": "Knuckles begins to disengage from the fight. He edges his way towards the back window. Continue the combat. If your opponent was the last person to take their combat action, it is now your turn and vice versa. His Fighting skill is 40/20. Carry out an opposed Fighting roll.",
        "choices": [{
            "opposed_roll": "Fighting",
            "opponent_skill": {"full": 40, "half": 20},
            "outcomes": {
                "win": {"goto": 64},
                "lose": {"goto": 103},
                "draw": {"goto": 103}
            }
        }]
    },
    17: {
        "text": "You tell the parking warden that you are on official business and ask if she is often in this area late in the evening. Disappointed, she jabs her stylus at a small notice on a pole across the road that says \"Permit holders only until 11 pm.\" She replies, \"So, yes.\" You ask if she has noticed any recent disturbances. You are going to make a Luck roll.",
        "choices": [{
            "luck_roll": True,
            "results": {
                "3": {"goto": 25},
                "2": {"goto": 36}
            }
        }]
    },
    18: {
        "text": "You tell Mrs Fellaman that you overheard an argument and a violent exchange, and you intend to enter her residence to assess the situation. \"No,\" she snaps. \"Bugger off.\" You inform her that you have reason to believe she is consorting with a spirit, in contravention of the Act against Conjuration, Witchcraft, and Dealing with Evil and Wicked Spirits 1604. Hopefully, Mrs Fellaman is not up to date on the legislation, as the Act was superseded in 1735. Her shoulders slump. \"You'd better come in,\" she says.",
        "choices": [{"goto": 10}]
    },
    19: {
        "text": "There is little room to back off. You raise your hand and issue a verbal warning with the authority they taught you at Hendon. Few villains are stupid enough to think that assaulting a police officer will in any way improve their situation. Unfortunately, Knuckles is one of that rare breed. He swings the hammer.",
        "choices": [{"goto": 4}]
    },
    20: {
        "text": "It's another 30 seconds before Mrs Fellaman seems satisfied that you are not there to lure her into an ambush. She returns to the doorway and gives you a suspicious stare. \"You're very quiet, aren't you?\" she says. \"What do you want?\"",
        "choices": [{"text": "Perguntar sobre o hematoma na bochecha da Sra. Fellaman", "goto": 50}, {"text": "Procurar por algo que possa facilitar uma entrada ilícita", "goto": 71}, {"text": "Perguntar sobre os 'dois rapazes'", "goto": 76}, {"text": "Insistir em olhar dentro da casa", "goto": 82}]
    },
    21: {
        "text": "After long nights attempting to push over empty cans of fizzy drink from a distance, you progressed to long nights successfully pushing over full cans of fizzy drink from a distance. Molly was not pleased about the sticky floor, but you can achieve an effective cast of Impello every time, particularly if you are thirsty.",
        "choices": [{"goto": 41}]
    },
    22: {
        "text": "You tell Mrs Fellaman that you are aware her flat is haunted, and you are a specialist who can help her to deal with the offending spectre. She curls her lip. \"I don't want any help,\" she says. You remind her that everybody is very concerned for her welfare and, if the disturbances continue, the neighbours will bring in the police; also, she has a finite supply of crockery. This last point seems to strike home. \"I wouldn't want my Charles and Di wedding plate to get chipped,\" she says. \"All right. You'd better come in.\"",
        "choices": [{"goto": 10}]
    },
    23: {
        "text": "You step, pivot, and twist the hammer as far as you can. Knuckles gasps and drops it. You have the presence of mind to whip your foot out of the way as the hammer slams against the floorboards. You have disarmed your opponent.",
        "choices": [{"goto": 39}]
    },
    24: {
        "text": "You back up to the other side of the yard and try to see what is banging around behind the bins. Molly watches your heroics like a cat studies a mortally wounded pigeon. The animal if that is what it is seems to have quietened down. Make an Observation roll.",
        "choices": [{
            "roll": "Observation",
            "results": {
                "5": {"goto": 47},
                "4": {"goto": 47},
                "3": {"goto": 47},
                "2": {"goto": 53},
                "1": {"goto": 53}
            }
        }]
    },
    25: {
        "text": "\"Funny you should ask,\" she says. \"I've seen a couple of shady characters hanging around over there.\" She points the stylus across the road again. \"Not unusual for dealers to nip down the basement stairs to make a sale. But these two were more like... what would you call them... enforcers? The guys who break your leg to persuade you to pay up.\" Interesting. You cross the road.",
        "choices": [{"goto": 107}]
    },
    26: {
        "text": "You concentrate on pushing Knuckles in the chest. \"Impello!\" Spend 1 magic point. Make a Magic skill roll. Since you have mastered Impello, you may have a bonus dice.",
        "choices": [{
            "text": "Make a Magic skill roll.",
            "effects": [{"action": "spend_magic", "amount": 1}],
            "roll": "Magic",
            "bonus_dice": True,
            "results": {
                "5": {"goto": 32},
                "4": {"goto": 32},
                "3": {"goto": 32},
                "2": {"goto": 56},
                "1": {"goto": 56}
            }
        }]
    },
    27: {
        "text": "You tell Mrs Fellaman you are aware her flat is haunted, and that you are a specialist who can help her deal with the offending spectre. \"It's none of your business,\" she says. \"Crock off, will you?\" The door slams in your face. Ernie stares at you from the car window. He seems unimpressed.",
        "choices": [{"text": "Se ainda não tentou, ir pelos fundos", "goto": 33}, {"text": "Tentar atraí-la para fora batendo na janela", "goto": 70}, {"text": "Caso contrário, realizar uma entrada forçada", "goto": 104}]
    },
    28: {
        "text": "You struggle to block the hammer. Knuckles grits his teeth and snarls. You may spend Luck to reduce your roll enough to increase your level of success. If you do this, go to 8. If you do not wish to spend Luck, the character who is taking their action wins and the character who is responding loses. So, if it is your action, you win. Go to 8. If it is Knuckles' action and you are responding, you lose. Go to 12.",
        "choices": [{"text": "Gastar Sorte para vencer a disputa", "goto": 8}, {"text": "Não gastar Sorte (Knuckles poderá ganhar a disputa).", "goto": 12}]
    },
    29: {
        "text": "You get a good look into the shadowy space behind the bins. It is a dark nest feathered with shredded packaging, and at its heart lurks a Yorkshire terrier. This is not Toby. This is some manner of grubby devil dog, with face markings not unlike the kind of cartoon masked burglars who used to walk around with huge sacks reading SWAG. The dog notices you and emerges from its lair, growling deep in its throat.",
        "choices": [{"goto": 77}]
    },
    30: {
        "text": "Apple crumble has not tasted the same since you spent long nights with Nightingale, attempting to fix an apple atop a candlestick while he swung his cricket bat at it. You have developed some fluency with Scindere.",
        "choices": [{"goto": 41}]
    },
    31: {
        "text": "While Mrs Fellaman's back is turned, you take the opportunity to pop your head inside the door. You glimpse a mean little corridor which opens into a mean little living room/kitchen combination. There are no obvious signs of a struggle. You pull back just as Mrs Fellaman turns around. She gives you a suspicious look as she returns to the doorway.",
        "choices": [{"text": "Perguntar sobre o hematoma", "goto": 50}, {"text": "Esperar pacientemente que ela o convide para entrar", "goto": 61}, {"text": "Perguntar sobre os 'dois rapazes'", "goto": 76}, {"text": "Insistir em olhar dentro da casa", "goto": 82}]
    },
    32: {
        "text": "Knuckles opens his eyes wide in surprise as he is shoved by an invisible hand. The hammer drops from his grasp. Make a Power (POW) roll.",
        "choices": [{
            "roll": "POW",
            "results": {
                "5": {"goto": 37},
                "4": {"goto": 37},
                "3": {"goto": 37},
                "2": {"goto": 45},
                "1": {"goto": 45}
            }
        }]
    },
    33: {
        "text": "Accessing the rear of Mrs Fellaman's flat is not straightforward. It is one in a row of private gardens protected by a brick wall, a serious knot of shrubbery, and a locked wooden gate stained a pleasing cherry red. You could deal with the lock, but the simplest thing might be to go over the wall. You wait for the street to clear of passers-by. A mother with a young child is the last straggler. As she bends to adjust something in her buggy, you swing your leg up and brace yourself on the wall. Make an Athletics roll.",
        "choices": [{
            "roll": "Athletics",
            "results": {
                "5": {"goto": 38},
                "4": {"goto": 38},
                "3": {"goto": 44},
                "2": {"goto": 49},
                "1": {"goto": 49}
            }
        }]
    },
    34: {
        "text": "Knuckles prowls the living room, watching your movements for any sign of weakness. He feints with the business end of his hammer. Continue the combat. If Knuckles has just taken his action, it is now your action and vice versa. His Fighting skill is 40/20. Decide whether you want to disarm your opponent or flee. If you have already refused an opportunity to flee, you must attempt to disarm. Whether it is his turn to act or respond, Knuckles tries to damage you. Carry out an opposed Fighting roll. Knuckles makes a Fighting roll and gets a fail.",
        "choices": [{
            "opposed_roll": "Fighting",
            "opponent_skill": {"full": 40, "half": 20},
            "outcomes": {
                "win": {"goto": 8},
                "lose": {"goto": 12, "effects": [{"action": "take_damage", "amount": 2}]},
                "draw": {"goto": 28}
            }
        }]
    },
    35: {
        "text": "You ask about the two boys Mrs Fellaman referred to. She gives the street one last look and then returns to the doorway. \"Toerags,\" she says. \"Claimed I owe them money. I've never seen them before in my life. If they come back I'll give them something they won't like.\" Door-to-door scams are still popular in the area, particularly those that target the elderly. But this particular lady does not seem taken in by them.",
        "choices": [{"text": "Perguntar sobre o hematoma", "goto": 50}, {"text": "Esperar pacientemente que ela o convide para entrar", "goto": 61}, {"text": "Procurar por algo que possa facilitar uma entrada ilícita", "goto": 71}, {"text": "Insistir em olhar dentro da casa", "goto": 82}]
    },
    36: {
        "text": "\"Sure,\" she says. \"Guy on the second floor uses a super soaker on anybody playing grime with their car windows open. Passing beards get physical about sourdough recipes. Old geezer walks a chihuahua that feels threatened by railings and footwear. I see all life here.\" You thank her for her diligence and cross the road.",
        "choices": [{"goto": 107}]
    },
    37: {
        "text": "Knuckles flies backwards through the air. His leg snags on an armchair and he flails, crashing to the ground head first. He stops moving. The hammer bumps on the carpet in front of you. You turn to the second assailant. Your successful POW roll increased the spell's effect.",
        "choices": [{"goto": 99}]
    },
    38: {
        "text": "You vault the wall in a single, clean movement, avoiding the foliage and landing catlike on the other side of the gate. After this Olympic-level performance, it is a simple matter to thread your way from garden to garden, counting the fences until you are level with the rear of Mrs Fellaman's flat.",
        "choices": [{"goto": 65}]
    },
    39: {
        "text": "Irate at the loss of his hammer, Knuckles advances, fists raised. His boxing stance is informed more by trashy cinema than any commitment to the gym. Knuckles jabs at your face. If he has already taken his action, it is now your action and vice versa. If the last thing you did was cast a spell, it is now Knuckles' action. His Fighting skill is 40/20. Decide whether you want to damage your opponent or restrain him. Now, carry out an opposed Fighting roll.",
        "choices": [
            {
                "text": "Attack (Damage)",
                "opposed_roll": "Fighting",
                "opponent_skill": {"full": 40, "half": 20},
                "outcomes": {
                    "win": {"goto": 54},
                    "lose": {"goto": 48, "effects": [{"action": "take_damage", "amount": 1}]},
                    "draw": {"goto": 48}
                }
            },
            {
                "text": "Try to immobilize (Restrain)",
                "opposed_roll": "Fighting",
                "opponent_skill": {"full": 40, "half": 20},
                "outcomes": {
                    "win": {"goto": 59},
                    "lose": {"goto": 48, "effects": [{"action": "take_damage", "amount": 1}]},
                    "draw": {"goto": 48}
                }
            }
        ]
    },
    40: {
        "text": "A hairy missile with teeth launches from behind the bins. You throw yourself out of its path. Make a Dexterity (DEX) roll.",
        "choices": [{
            "roll": "DEX",
            "results": {
                "5": {"goto": 58},
                "4": {"goto": 58},
                "3": {"goto": 58},
                "2": {"goto": 68},
                "1": {"goto": 68}
            }
        }]
    },
    41: {
        "text": "Mrs Fellaman emerges from the kitchen holding a white-enamel camping mug and the kind of plastic cup that comes from the top of a Thermos flask. You sit down at the table. China crunches beneath your feet. \"Sorry I'm out of real cups,\" she says. Her teapot has somehow survived. As the tea brews she offers you a custard cream. You take one and ask about the ghost. \"He's my husband,\" she says, the edge of her mouth curling. \"Victor. He first showed up three months ago. Always at night. Same as he ever was. Quieter maybe.\" You lead the conversation slowly to the bruise on her cheek. She touches it as if she had forgotten it was there. \"We always used to row, you know, some people you just row with-I suppose even him being passed on couldn't change that. He made me so cross. I, uh...\" She looks sheepish. \"I forgot he was a ghost. I ran right through him, hit the wall, and fell over. You know how it is, you grab the nearest thing. That was the cupboard. It fell over, and then I had the Old Bill knocking at my door.\" Your custard cream is finished. You ask Mrs Fellaman to summon her husband for you. \"You're joking,\" she says. \"He comes and goes when he wants-always did.\" You push back your chair, stand up, and open your palm. You need a werelight to draw out the ghost. As there is no time pressure on you to cast the Werelight spell, there is no need to make a Magic roll to see if you are successful. Spend 1 magic point.",
        "choices": [{"goto": 51}]
    },
    42: {
        "text": "You tell the traffic warden you are a social worker visiting a family across the road. Her expression does not change. \"So, not delivering primary healthcare?\" she asks, stylus poised above her battered handheld computer.",
        "choices": [{"goto": 52}]
    },
    43: {
        "text": "Knuckles is a little too slow this time. You catch his forearm and immobilise it. If you already had Knuckles restrained, and you are a Police Officer, go to 105. If you already had Knuckles restrained, and you are a Nurse or Social Worker, go to 84. Otherwise, continue the combat, but give Knuckles a penalty dice for the remainder of the fight. You may attempt a further combat manoeuvre to restrain Knuckles completely.",
        "choices": [{"text": "Se Knuckles já estava contido e você é Policial", "goto": 105}, {"text": "Se Knuckles já estava contido e você é Enfermeiro ou Assistente Social", "goto": 84}, {"text": "Caso contrário, continuar o combate", "goto": 16}]
    },
    44: {
        "text": "You vault the wall, but your foot snags on a shrub and you topple down the far side of the gate. Your wrist bends back at impact.",
        "choices": [{"text": "Se você é Enfermeiro", "goto": 55}, {"text": "Caso contrário", "goto": 60}]
    },
    45: {
        "text": "Knuckles stumbles back, collapsing into an armchair. His hammer hits the carpet. You can see him fail to process what just happened. He falls back on what he knows, getting back to his feet and closing for a fist fight. Still, you have successfully disarmed him. Although your POW roll was unsuccessful, the spell still had a minor effect.",
        "choices": [{"goto": 39}]
    },
    46: {
        "text": "You explain to Mrs Fellaman that you would like to come in to talk about the previous night's disturbance. She returns to the doorway. \"I've already spoke to the other copper,\" she says. By this she means the sergeant whose perceptive report led to your involvement. You try again to invite yourself into the house. Mrs Fellaman plants her feet and folds her arms.",
        "choices": [{"text": "Perguntar sobre o hematoma", "goto": 50}, {"text": "Esperar pacientemente", "goto": 61}, {"text": "Procurar entrada ilícita", "goto": 71}, {"text": "Perguntar sobre os 'dois rapazes'", "goto": 76}]
    },
    47: {
        "text": "From this distance you see little movement behind the bins. Something rustles quietly in the shadows, but it could easily be the wrapping from a Marks & Spencer vegetable biryani. Then you glimpse it out of the corner of your eye, moving fast and low against the ground. It passes beneath a window, and you recognise that the bin fiend is a dog. But not Toby. This is a scrappy Yorkshire terrier, with the kind of face that Cerberus might pull upon learning he has been resurrected in miniature with only one head.",
        "choices": [{"goto": 77}]
    },
    48: {
        "text": "Knuckles throws a torrent of punches. You are knocked back against the table. Mark down that you take 1 damage. If you have suffered 1 damage in total, you are Hurt. If you have suffered 2 damage in total, you are Bloodied. If either of these, go to 67. If you have suffered 3 damage in total, you are Down. Go to 95.",
        "choices": [{"text": "Se o dano total for 1 ou 2", "goto": 67}, {"text": "Se o dano total for 3", "goto": 95}]
    },
    49: {
        "text": "With a brave effort, you get up on the wall, but you misjudge the height of the gate. Your supporting foot snags on a branch and you tumble, landing on your back on the pavement. A teenage boy in a Tottenham Hotspur strip (jersey) rounds the corner, dribbling a football (soccer ball). Seeing you sprawled there, he pauses. Then he bounces his ball off the gate and dodges around your head, beating an imaginary defender. You get to your feet. A neighbour peers from their kitchen window to see what all the noise is.",
        "choices": [{"text": "Se ainda não tentou, voltar e bater na porta", "goto": 13}, {"text": "Caso contrário, realizar uma entrada forçada", "goto": 104}]
    },
    50: {
        "text": "Mrs Fellaman turns her head away as you ask about the bruise. She very deliberately does not lift her hand to her cheek. \"I walked into the door, didn't I?\" she says. \"You get like that when you're a bit older.\" You find a gentle way to say that neither of you believes that. She does not relent. But she doesn't argue with you either.",
        "choices": [{"goto": 88}]
    },
    51: {
        "text": "A small and very bright sphere appears in your hand, the size of a golf ball. From experience, you know its energy is irresistible to ghosts. You place the werelight on the table. Mrs Fellaman stares at it wide-eyed. \"What's that?\" she asks. Before you can answer, the ball of light darkens to a dim crimson. A ghost is feeding on its energy. You look around. A man stands against the side wall, looking at you with apparent amazement. He is young, early 20s, wearing a rather nice suit. He looks like he could feature on the Wikipedia page which defines the Mod subculture. You raise an eyebrow at Mrs Fellaman. \"What?\" she says. \"He looks just like he did when I met him.\" You look ghost-Victor over from head to toe. Your gaze stops on his shoes. They're old, worn, brown; too big for his feet. Clumpy. No self-respecting Mod would wear those shoes.",
        "choices": [{"text": "Perguntar ao fantasma sobre a Sra. Fellaman", "goto": 63}, {"text": "Perguntar ao fantasma por que ele está aqui", "goto": 93}, {"text": "Desligar o werelight", "goto": 101}]
    },
    52: {
        "text": "You explain that this is a preliminary visit to a new client. The warden points her stylus at a small notice on a pole across the road. \"Permit holders only until 11 pm,\" she says. \"Do you have a permit for zone CA-F?\" You are going to make a Luck roll.",
        "choices": [{
            "luck_roll": True,
            "results": {
                "3": {"goto": 57},
                "2": {"goto": 66}
            }
        }]
    },
    53: {
        "text": "You keep your eye on the dark recess behind the bins. Things seem to have quietened down. A shadow flops, the torn remains of a box catching an air current. Where is the creature that was enacting such loud violence a few seconds ago? A hairy missile with teeth erupts from the ground beside you. You throw yourself out of its path. Make a Hard Dexterity (DEX) roll.",
        "choices": [{
            "roll": "DEX",
            "difficulty": "hard",
            "results": {
                "5": {"goto": 58},
                "4": {"goto": 58},
                "3": {"goto": 58},
                "2": {"goto": 68},
                "1": {"goto": 68}
            }
        }]
    },
    54: {
        "text": "Your fist catches Knuckles on the ear. He yowls and cups a hand over it. Mark down on some scrap paper that you have inflicted 1 damage to Knuckles. If you have inflicted 3 or more damage in total, your opponent drops to the ground. Go to 99. Otherwise, go to 67.",
        "choices": [{"text": "Se o dano total for 3 ou mais", "goto": 99}, {"text": "Caso contrário", "goto": 67}]
    },
    55: {
        "text": "You have seen this injury hundreds of times a reflexive thrust of the hand to break a fall. At its worst, it results in a broken collarbone, but you have a simple wrist sprain. Only rest will fix it permanently, but you can make do for now with one of the bandages you keep about your person. Nobody from the corner flat comes out to investigate while you sit in their garden applying the bandage for compression. You flex your fingers. This will be all right until you get home. Favouring your other hand, you work from garden to garden, counting the fences until you are level with Mrs Fellaman's flat.",
        "choices": [{"goto": 65}]
    },
    56: {
        "text": "Under pressure, you sometimes find it hard to shape the forma. The hammer arcing towards your head represents a significant amount of pressure. This time, the spell eludes you. You must deal with your attacker, hand-to-hand.",
        "choices": [{"goto": 4}]
    },
    57: {
        "text": "You are forced to concede that you do not possess the appropriate permit. Yet the warden hesitates. \"Wait a minute. Social worker? What's that like? My sister's looking for a job.\" You explain that the role is one of support and problem-solving, rooted in social and interpersonal difficulties. It requires careful record-keeping and liaison with a wide range of other services and agencies, under pressure from shrinking budgets. At heart, the work aims for a more equal and just society. \"Oh right. Forget it then. She's pretty social, but not much of a worker, if you know what I mean.\" The warden looks in both directions. \"I'll miss you this time, love, OK? Don't be here in an hour.\" She walks off. You cross the road.",
        "choices": [{"goto": 107}]
    },
    58: {
        "text": "You duck and roll across the yard, while the snarling ball of grubby trouble soars through the space you recently occupied. As you rise, you recognise your assailant as a Yorkshire terrier-with a stare that would be at home in any post-apocalyptic thriller. You face up to the beast.",
        "choices": [{"goto": 77}]
    },
    59: {
        "text": "You sidestep Knuckles' punch and get a lock on his arm. You try to force him to the ground. He continues to lash out at your legs and stomach. Continue the combat, but give Knuckles a penalty dice for the remainder of the fight. You may attempt a further combat manoeuvre to restrain Knuckles completely.",
        "choices": [{"goto": 67}]
    },
    60: {
        "text": "You flex your injured hand and grimace at the surge of pain. You should probably apply ice to stop it swelling, but none is available while you squat here on the paving of a stranger's back garden. The sooner you can deal with this situation, the sooner you can get the injury looked at. You press on from garden to garden, counting the fences until you are level with Mrs Fellaman's flat. Until you leave Prince of Wales Road, you must add a penalty dice to your Fighting rolls.",
        "choices": [{"goto": 65, "effects": [{"action": "apply_penalty", "skill": "Fighting", "duration": 1}]}]
    },
    61: {
        "text": "You glance at the neighbouring properties in the manner of one who is concerned about confidentiality. The silence stretches out. Mrs Fellaman gives you the kind of stare perfected by those with a preference for marmalade sandwiches. She shows no inclination whatsoever to relocate the conversation.",
        "choices": [{"goto": 88}]
    },
    62: {
        "text": "Knuckles is wary of you now. The two of you crash around the living room, trading punches while crockery crunches beneath your feet. His heel snags on the fireplace and you take the opportunity to seize Mrs Fellaman's carriage clock and smash him over the head. Mark down on some scrap paper that you inflict 1 damage to Knuckles. If you have inflicted 3 or more damage in total, your opponent drops to the ground. Go to 99. Otherwise, go to 16.",
        "choices": [{"text": "Se o dano total for 3 ou mais", "goto": 99}, {"text": "Caso contrário", "goto": 16}]
    },
    63: {
        "text": "The man at the wall hesitates. He doesn't answer your questions about Mrs Fellaman. \"What do you want?\" he asks. Something is wrong with his accent too. It is not the kind of '60s cockney twang that would fit with the suit and Eugenia Fellaman. You glance at the werelight. While the conversation continues, you are feeding magic to this ghost.",
        "choices": [{"text": "Perguntar ao fantasma por que ele está aqui", "goto": 93}, {"text": "Desligar o werelight", "goto": 101}]
    },
    64: {
        "text": "Knuckles flees to the window and turns his back to clamber out. You vault over the settee and reach him in time to slam his head against the frame. Mark down on some scrap paper that you inflict 1 damage to Knuckles. If you have inflicted 3 or more damage in total, your opponent drops to the ground. Go to 99. Otherwise, go to 103.",
        "choices": [{"text": "Se o dano total for 3 ou mais", "goto": 99}, {"text": "Caso contrário", "goto": 103}]
    },
    65: {
        "text": "The flat has a small rear garden which looks like it was tended with care until recently. You try the kitchen door. It is unlocked. You announce your presence and step inside the flat. Mrs Fellaman appears in the doorway to the living room. She looks defeated. \"Can't take a hint, can you?\" she says. \"Well, I suppose you better come in.\"",
        "choices": [{"goto": 10}]
    },
    66: {
        "text": "You are forced to concede that you do not possess the appropriate permit. The traffic warden taps her teeth with the council-issued stylus and checks her watch. Defeated, you return to the car and ease it out of the space. After 20 minutes of circling, you find an incredibly tight space three streets away. Local kids sitting on a wall eye the Escort's removable components. Judging by their expressions of disgust, you have nothing to fear. You make your way on foot back to the address on Prince of Wales Road.",
        "choices": [{"goto": 107}]
    },
    67: {
        "text": "Knuckles spits, breathing hard. You are not the easy victim he expected. Continue the combat. If your opponent was the last person to take their action, it is now your turn and vice versa. Knuckles' Fighting skill is 40/20. On your turn, decide whether you want to damage your opponent or restrain him. On his turn, Knuckles tries to damage you. Carry out an opposed Fighting roll.",
        "choices": [
            {
                "text": "Attack (Damage)",
                "opposed_roll": "Fighting",
                "opponent_skill": {"full": 40, "half": 20},
                "outcomes": {
                    "win": {"goto": 62},
                    "lose": {"goto": 89, "effects": [{"action": "take_damage", "amount": 1}]},
                    "draw": {"goto": 89}
                }
            },
            {
                "text": "Try to immobilize (Restrain)",
                "opposed_roll": "Fighting",
                "opponent_skill": {"full": 40, "half": 20},
                "outcomes": {
                    "win": {"goto": 43},
                    "lose": {"goto": 89, "effects": [{"action": "take_damage", "amount": 1}]},
                    "draw": {"goto": 89}
                }
            }
        ]
    },
    68: {
        "text": "You don't move fast enough. As its limbs splay in mid-air, you identify a Yorkshire terrier, with a face constructed from a shaggy nightmare. It clips your ribs and knocks you spinning. Pain flares up your leg as you get to your feet. You were knocked prone by the dog's attack. This leaves you particularly vulnerable to further attacks. However, when it is your turn to act, you may stand up as a free action.",
        "choices": [{"goto": 77}]
    },
    69: {
        "text": "You concentrate on fixing the hammer in space. \"Scindere!\" Spend 1 magic point. If you want to boost the spell for greater effect, spend 1 additional magic point. Update your current magic points accordingly. Make a Magic skill roll. Since you have mastered Scindere, you may have a bonus dice.",
        "choices": [{
            "text": "Cast Scindere",
            "effects": [{"action": "spend_magic", "amount": 1}],
            "roll": "Magic",
            "bonus_dice": True,
            "results": {
                "3": {"goto": 86},
                "2": {"goto": 97},
                "1": {"goto": 97}
            }
        },
        {
            "text": "Cast Scindere (Boosted)",
            "effects": [{"action": "spend_magic", "amount": 2}],
            "roll": "Magic",
            "bonus_dice": True,
            "results": {
                "3": {"goto": 80},
                "2": {"goto": 97},
                "1": {"goto": 97}
            }
        }]
    },
    70: {
        "text": "This may not be the most professional move of your career. However, it might put some distance between the householder and whatever has manifested inside her residence. Looking around for a hiding place, you consider the steps above her door, which lead to the flats above. You would be in plain sight, but only if Mrs Fellaman looks directly up. Worth a try. From inside, you hear another plate smash. You rap on the window then flee up the stairs. You have barely reached your refuge when Mrs Fellaman bursts from the door, moving faster than you expected. She appears to have a cricket bat.",
        "choices": [{"goto": 74}]
    },
    71: {
        "text": "There is a hook on the wall behind Mrs Fellaman, upon which hangs a ring with two Yale keys. The letterbox has no brushes. An enterprising burglar with a long, hooked stick and a steady hand might enter with minimal force-or a magically-skilled investigator looking for a conventional solution. She follows your gaze over her shoulder and down the back of the door. \"What?\" she asks.",
        "choices": [{"goto": 88}]
    },
    72: {
        "text": "You tell the traffic warden you are a nurse attending a new patient across the road. The warden points her stylus at your rear-view mirror. \"You're not displaying the Health Emergency Badge,\" she says.",
        "choices": [{"goto": 81}]
    },
    73: {
        "text": "You put an armchair between yourself and Knuckles, bolt for the door, and throw it open. You scramble out onto Prince of Wales Road, where the sounds of struggle have already attracted a few passers-by. One is on their phone, presumably to the emergency services. You are still an apprentice in the ways of magic, and you have successfully escaped a dangerous situation. You can call in reinforcements. But this will not go down as a glorious day in your career with the Folly. Mrs Fellaman's voice splits the air, screaming at the intruders. From the thump of wood against flesh and the whining of low-level toughs, she is giving as good as she gets. You have failed to get to the bottom of what's happening at Prince of Wales Road. Don't worry if things didn't turn out for the best-you can always return to the beginning and try again, perhaps choosing a different occupation. Good luck! THE END.",
        "choices": []
    },
    74: {
        "text": "Mrs Fellaman steps up to the pavement, brandishing her willow-and-linseed-oil weapon with serious intent. \"I told you boys I'm not paying!\" she yells, scanning in both directions. A passing cyclist swerves, narrowly missing the Escort. She notices Ernie and steps closer to the car, eyeing the hairy terror. For a moment you visualise the paperwork that will result if the pensioner you were supposed to be protecting initiated an armed brawl with a stray dog you had acquired. Then she turns around and spots you on the stairs. Her jaw sets.",
        "choices": [{"text": "Se você é Assistente Social", "goto": 79}, 
        {
            "roll": "Social",
            "results": {
                "5": {"goto": 83},
                "4": {"goto": 83},
                "3": {"goto": 87},
                "2": {"goto": 91},
                "1": {"goto": 91}
            }
        }]
    },
    75: {
        "text": "Confusion breaks across Knuckles' face as the spell takes hold and the hammer locks into place in the air.",
        "choices": [{"text": "Se você aumentou o feitiço", "goto": 80}, {"text": "Caso contrário", "goto": 86}]
    },
    76: {
        "text": "You ask about the two boys Mrs Fellaman referred to earlier. She wrinkles her nose. \"Toerags,\" she says. \"Claimed I owe them money. I've never seen them before in my life. If they come back, I'll give them something they won't like.\" Door-to-door scams are still popular in the area, particularly those that target the elderly. But this particular lady does not seem susceptible to social engineering.",
        "choices": [{"goto": 88}]
    },
    77: {
        "text": "As you confront the terrier, you experience three rapid insights. First, a nametag glints beneath the grimy leather of its collar. Second, a dog that is drawn to the Folly probably has some innate magic sensitivity. Third, it has noticed your packet of artisan sausages, and its eyes are fixed on the gleaming plastic wrap. You pull open the packet and extract a sausage for the hungry dog. You could make an Animal Handling roll to subdue the Yorkshire terrier-but you do not possess this expert skill. You may instead Try Your Luck.",
        "choices": [{"text": "Tentar a Sorte (Try Your Luck) para usar Animal Handling", "goto": 85}, {"text": "Não gastar Sorte", "goto": 98}]
    },
    78: {
        "text": "Your legs buckle and you fall into nothingness. When your vision returns, you are staring at the light in the centre of Mrs Fellaman's ceiling. Your head pounds. Her face looms into view, creating an impromptu eclipse. \"When you got mashed by that hammer, I thought you were a goner,\" Mrs Fellaman says. \"Get off my carpet so I can sweep up.\" She offers you a wiry hand. Your attackers appear to have left. Because you were Down at the end of the fight, you remain Hurt for the rest of the day.",
        "choices": [{"goto": 110}]
    },
    79: {
        "text": "This is not the first time you have faced down an irate senior citizen wielding a cricket bat. You are able to push aside immediate worries about head injuries and concussion in order to take a professional approach.",
        "choices": [{"goto": 83}]
    },
    80: {
        "text": "Your onrushing attacker runs straight into the masonry hammer, literally hitting himself in the face. He goes down like a coyote in a cartoon. You turn to the second assailant.",
        "choices": [{"goto": 99}]
    },
    81: {
        "text": "The Ford Escort you are using on this occasion does not have the stock of blank badges you use on NHS (National Health Service) business. You go through your pockets for a spare. The warden watches you search. \"It needs to display the address or it's not valid,\" she comments unnecessarily. You are going to make a Luck roll.",
        "choices": [{
            "luck_roll": True,
            "results": {
                "3": {"goto": 90},
                "2": {"goto": 94}
            }
        }]
    },
    82: {
        "text": "You insist to Mrs Fellaman that you would like to come in and talk about the previous night's disturbance. She remains in the doorway. \"I've already spoke to the other copper,\" she says. By this she means the sergeant whose perceptive report led to your involvement. You try again to invite yourself into the house. Mrs Fellaman plants her feet and folds her arms.",
        "choices": [{"goto": 88}]
    },
    83: {
        "text": "Using your conflict resolution training, you frame your actions as extracting Mrs Fellaman from a hazardous situation. You explain that your presence, however she might resent it, represents the support of her community, and that her nightly quarrels with a ghost are unsustainable both in terms of disturbing the neighbours and her personal health. The fight seems to go out of Mrs Fellaman. She leans on the cricket bat and touches her bruised face. \"I know that,\" she says. \"I just didn't want it to end yet.\" She gives a long sigh. \"I suppose you'd better come in.\"",
        "choices": [{"goto": 10}]
    },
    84: {
        "text": "You kick Knuckles' ankles from beneath him, and his face hits the floor. He continues to wriggle like a fish out of water until Mrs Fellaman pushes past you and administers the coup de grace to his head with her cricket bat. The resulting \"whack\" would be familiar to any spectator at The Oval cricket ground. Knuckles is Down. The second intruder is long gone.",
        "choices": [{"goto": 110}]
    },
    85: {
        "text": "You display the sausage and hold up a finger to indicate the terrier should behave. Your finger looks uncomfortably like a second sausage. Subtract 10 points from your current Luck. You will use your Intelligence (INT) or Power (POW) characteristic (whichever is highest) to attempt Animal Handling, even though you don't possess this expert skill. Try Your Luck by making a Hard roll against INT or POW (whichever is highest).",
        "choices": [
                      {
                "text": "Try Your Luck by making a Hard roll against INT.",
                "effects": [{"action": "spend_luck", "amount": 1}],
                "roll": "INT",
                "difficulty": "hard",
                "results": {
                    "5": 92,
                    "4": 92,
                    "3": 92,
                    "2": 98,
                    "1": 98
                }
            },
            {
                "text": "Try Your Luck by making a Hard roll against POW.",
                "effects": [{"action": "spend_luck", "amount": 1}],
                "roll": "POW",
                "difficulty": "hard",
                "results": {
                    "5": 92,
                    "4": 92,
                    "3": 92,
                    "2": 98,
                    "1": 98                
                }
            }
        ]
    },
    86: {
        "text": "Knuckles hauls at the hammer, unable to comprehend the force holding it frozen in space. He gives it a few more pulls before turning to face you. You have successfully disarmed your opponent.",
        "choices": [{"goto": 39}]
    },
    87: {
        "text": "You try to reassure Mrs Fellaman that you have only her best interests at heart. She swings the bat at you, but you can see her rage and the strength behind each blow-dissipating. To dodge the cricket bat, make a Fighting roll. As Mrs Fellaman is conflicted about the fight, you may apply a bonus dice to your roll.",
        "choices": [{
            "roll": "Fighting",
            "bonus_dice": True,
            "results": {
                "5": {"goto": 96},
                "4": {"goto": 96},
                "3": {"goto": 96},
                "2": {"goto": 100},
                "1": {"goto": 100}
            }
        }]
    },
    88: {
        "text": "\"I've got a pot on the stove,\" Mrs Fellaman says. You tell her that everybody is concerned about her safety. \"That's nice,\" she says. \"But it's my patience you should be worried about. That other copper looked all over the house, and she found nothing. Haven't you got anything better to do than harass an old age pensioner?\" You adopt a particularly patient tone while explaining you're there to help. \"I'm sick of your help,\" she says. \"Have you got a warrant or council notice or something?\" You admit that you have not. \"Then you can piss off,\" she says and closes the door in your face.",
        "choices": [{"goto": 102}]
    },
    89: {
        "text": "Knuckles closes in, shrugging off your blows to land a heavy punch against your stomach. You feel the breath rush out of you. Mark down that you take 1 damage. If you have suffered 1 damage in total, you are Hurt. If you have suffered 2 damage in total, you are Bloodied. Mark the appropriate boxes on your character sheet and go to 16. If you have suffered 3 damage in total, you are Down. Mark the Down box on your character sheet and go to 95.",
        "choices": [{"text": "Se dano total 1 (Hurt) ou 2 (Bloodied)", "goto": 16}, {"text": "Se dano total 3 (Down)", "goto": 95}]
    },
    90: {
        "text": "You find an old Health Emergency Badge in your jacket pocket. It is creased, dog-eared, and features a ring from a coffee mug across one corner, which is presumably why you never used it. You lean on the roof of the Escort to inscribe the address of your new client in painstakingly clear capital letters. The warden makes a point of lingering until you hang the HEB from the mirror of the Escort. Clinging to this token victory, she moves off. You cross the road.",
        "choices": [{"goto": 107}]
    },
    91: {
        "text": "Your attempts to calm Mrs Fellaman down only seem to increase her fury, and she steps towards you with her cricket bat raised. You have no alternative but to get out of the way.",
        "choices": [{"text": "Se ainda não tentou, recuar e ir pelos fundos", "goto": 33}, {"text": "Caso contrário, realizar entrada forçada", "goto": 104}]
    },
    92: {
        "text": "The terrier's attitude improves significantly once it realises it can obtain a sausage for good behaviour. After a bit of initial skittering around and snarling, it sits up and waits, trembling as it eyes the meaty reward. Three hard-earned sausages later, the dog is calm and compliant. To permanently gain the Animal Handling expert skill at half the appropriate skill value, spend a further 10 points of Luck.",
        "choices": [{"goto": 106, "effects": [{"action": "spend_luck", "amount": 10}, {"action": "gain_skill", "skill": "Animal Handling"}]}]
    },
    93: {
        "text": "The man's eyes flicker to the werelight and then to Mrs Fellaman. He doesn't answer. You have fed him enough magic. Time to wind this up.",
        "choices": [{"goto": 101}]
    },
    94: {
        "text": "You complete your search and admit you do not have a Health Emergency Badge to display. You show the warden your NHS identification card instead and appeal to her good nature. She taps her teeth with the council-issued stylus and checks her watch. Defeated, you return to the car and ease it out of the space. After 20 minutes of circling, you find a space behind a gardener's lorry three streets away. Before you can shut off the air conditioning, the car fills with the pungent stench of compost. You make your way on foot back to the address on Prince of Wales Road.",
        "choices": [{"goto": 107}]
    },
    95: {
        "text": "Knuckles grabs your collar and, spittle flying, headbutts you in the face. Everything goes dark. When you rise back to consciousness, something is lying on your face. You reach for it and find it to be the shaft of a standard lamp. The shade has been smashed. As you roll it aside, Mrs Fellaman drifts into view. \"I liked that lamp,\" she says. \"Got it from Harrods.\" She picks up the lamp without offering you any assistance. The attackers appear to have left. Because you were Down at the end of the fight, you remain Hurt for the rest of the day.",
        "choices": [{"goto": 110}]
    },
    96: {
        "text": "You duck under the last swing of the bat. Mrs Fellaman suddenly seems to feel its weight and lets it rest on the step beneath you. She slumps against the railing. You relieve her of the weighty bat and insist that you should enter the flat to assess the situation. \"I just got my blood up,\" she says. \"Sorry about trying to clobber you and all that.\" You return to the flat together.",
        "choices": [{"goto": 10}]
    },
    97: {
        "text": "Under pressure, you sometimes find it hard to shape the forma. The hammer arcing towards your head represents a significant amount of pressure. This time, the spell eludes you. You must deal with your attacker, hand-to-hand.",
        "choices": [{"goto": 4}]
    },
    98: {
        "text": "The terrier's response is swift and overwhelming. As it charges, you whip the sausage out of reach-but it is not aiming for your paltry single sausage. Its jaws clamp around the entire bag of sausages and its weight drags you off balance. You stumble and your head crashes against the wall. As you thump to the ground, the bag gives way and artisan sausages spill across the yard. After 30 seconds of deep breathing and cold personal reflection to a soundtrack of tearing plastic and meaty guzzling, you sit up. Most of the sausages are gone. The dog, however, is calmer. It sniffs and watches you mop blood from your temple. You are Hurt.",
        "choices": [{"goto": 106, "effects": [{"action": "take_damage", "amount": 1}]}]
    },
    99: {
        "text": "You turn to see Mrs Fellaman swing a cricket bat into the face of the second invader. He drops like wet laundry. She studies him for a moment before delivering a single, considered kick to his groin. \"Get out of it,\" she says. \"You'll get your money when I've got it.\" He stumbles to the rear window and topples out into the night. You hear creaks and moans as he retraces his path through strangers' gardens. Mrs Fellaman looks up at you. \"My fault,\" she says. \"I get a little frisky sometimes on the gee-gees. I'm none too particular who I take a loan from.\" You'll have to decide what to do with Knuckles, who is currently groaning on the carpet. But that can wait for later.",
        "choices": [{"goto": 110}]
    },
    100: {
        "text": "The cricket bat connects with your shoulder and slams you against the railing. Mrs Fellaman, at least, has the good manners to be appalled at what she has done. You take the bat from her hands and reassure her that no bones are broken. \"I just got my blood up,\" she says. \"Sorry about that. It wasn't really you I was mad at. I suppose you had better come in.\" You return to the flat together. You have suffered 1 damage and are Hurt. However, because the combat has ended, you immediately recover from your Hurt state.",
        "choices": [{"goto": 10, "effects": [{"action": "take_damage", "amount": 1}, {"action": "heal_damage", "amount": 4}]}]
    },
    101: {
        "text": "You ask the ghost what his mother's name is. He frowns and hesitates. \"What do you want to know for?\" he says. The hesitation tells you enough. You extinguish the werelight and \"Victor\" instantly fades to transparency. A whisper tickles the air. \"Martha.\" \"Bring him back,\" Mrs Fellaman says. You ask her if Victor's mother was named Martha. \"No.\" She looks sour. \"But he's dead. You're bound to forget-\" The back window shatters.",
        "choices": [{"goto": 6}]
    },
    102: {
        "text": "You return to the Ford Escort and settle behind the wheel to consider your options. After a minute, you unfold the report for another look. The Camden response team passed the details onto the local neighbourhood safety team, which is headed by a Sergeant Sutherland. You put a call into the local station and get her on the phone. Once you get past the initial wariness that most police have for agents of the Folly, she relaxes and opens up. \"I talked to the neighbours, confirmed their stories, made a follow-up visit to Mrs Fellaman, and found precisely nothing. And, since all I had on that night was leftover pasta bake, I parked my own car outside and waited until I heard the argument for myself.\" The sergeant's notes specify hearing two voices. But when Sutherland talked herself inside the flat, Mrs Fellaman was alone. \"That's right,\" she says. \"And I'll tell you, something was off about that flat.\" Members of the general public are regularly unsettled by inconsequential tosh. But Sergeant Sutherland's 30 years of experience in policing are as good a barometer for supernatural activity as you are likely to find. \"Your kind of weird bollocks,\" she says. Before you can take any further action on this case, such as an unauthorised entry to Mrs Fellaman's flat, you need to be sure that there is indeed some \"weird bollocks\" going on.",
        "choices": [{"goto": 5}]
    },
    103: {
        "text": "Knuckles dives through the open window. His compatriot seems long gone. You get to the window. Shrubs bend and fencing creaks. Groans punctuate his journey through the gardens of Prince of Wales Road. Mrs Fellaman comes up behind you, leaning on her cricket bat. \"Let him go,\" she says. \"I already sent his friend packing. And I do owe them the money. A couple of sure things at the races that didn't come in.\"",
        "choices": [{"goto": 110}]
    },
    104: {
        "text": "Walking away from a ghostly manifestation in progress is not an option, and you seem to have exhausted all of your alternatives except one. You examine Mrs Fellaman's door and the Yale lock that secures it. A more experienced magician could simply carve out the cylinder, but you will have to do it the old-fashioned way. You get a run-up as best you can and shoulder the door. It flies open with a crack, admitting you into the flat's narrow hallway. As you turn to survey the interior, a strange disc tumbles through the air. By the time you recognise it as a dinner plate with decorative bird illustrations, it is dangerously close to your face. You duck. Make a Fighting roll. If you fail, suffer 1 damage and become Hurt.",
        "choices": [{
            "roll": "Fighting",
            "results": {
                "5": {"goto": 108},
                "4": {"goto": 108},
                "3": {"goto": 108},
                "2": {"goto": 108, "effects": [{"action": "take_damage", "amount": 1}]},
                "1": {"goto": 108, "effects": [{"action": "take_damage", "amount": 1}]}
            }
        }]
    },
    105: {
        "text": "You kick Knuckles' ankles from beneath him, and his face hits the floor. Before he can wriggle out of it, you put a knee on his back and sling one cuff around his right wrist. A twist of the forearm brings the other wrist close enough to fasten the second cuff. Now to deal with the second assailant.",
        "choices": [{"goto": 99}]
    },
    106: {
        "text": "The dog does not resist as you crouch down and lift the brass tag on its collar. The tag is shaped like a cartoon bone and engraved with tight capital letters reading ERNIE. Satiated on sausages, Ernie seems more curious than aggressive. You look up at the coach house window. Molly is unmoved by your struggle. She makes a flittering hand gesture towards the gate to the street. Nobody around Russell Square appears to be looking for a lost dog. You can attempt to locate Ernie's owners once he has performed a quick service on the Folly's behalf. In the back of the Escort, you find a beach towel and spread it over the back seat. Ernie is content to hop inside, spraying flakes of grime as he goes. You borrow Toby's spare lead and get back into the car.",
        "choices": [{"goto": 2}]
    },
    107: {
        "text": "The Victorian terrace carries a certain dignity as it faces off against the new builds across the road. Its sash windows and ironwork look recently painted. The disturbance you are here to investigate came from the half basement below. You study the exterior. There are no external signs of a struggle. A door is crammed in below the steps to the main entrance a familiar construction in this area. That door was probably the tradesman's entrance before the house was divided into flats. The door has no bell, but it does have a large brass knocker mottled with verdigris. You lift it and knock.",
        "choices": [{"goto": 3}]
    },
    108: {
        "text": "Mrs Fellaman approaches, another plate in hand. She looks at the cracked doorframe and sighs. \"Don't know when to give up, do you? I thought you were one of them lads wanting money. I could have split your head open. Oh well, since you're here I'll make you a cup of tea. And then you can phone for a carpenter.\"",
        "choices": [{"goto": 10}]
    },
    109: {
        "text": "You shoulder Knuckles away and scramble out of range. In the process, you place a foot wrong and tumble to one knee among the fragments of crockery. As you stand back up, Knuckles sneers and turns his attention to Mrs Fellaman. She confronts the two intruders alone, her gaze following the hammer. Knuckles glances at you. \"You still here?\" he says. \"Beat it.\" If you are still at full health, take 1 damage from your fall, and so mark the Hurt box on your character sheet. Otherwise, your injuries are minor.",
        "choices": [
            {"text": "Fugir", "goto": 73, "effects": [{"action": "take_damage", "amount": 1, "condition": "full_health"}]},
            {"text": "Voltar para defender a Sra. Fellaman", "goto": 34}
        ]
    },
    110: {
        "text": "Mrs Fellaman is still holding a cricket bat spattered with fresh blood. She clicks her tongue and runs the bat's wooden surface under the cold tap. While she is distracted, you turn your attention back to her domestic ghost. Something bothers you about the wall where he appeared. You've been in flats built to the same plan, and they had a pantry alcove to the left of the bricked-up fireplace. \"What about my husband?\" Mrs Fellaman asks. Still eyeing the wall, you explain that you were briefed about her family history, and her husband left her 30 years ago. He is currently living in Prestatyn, Wales, with a woman named Blodwyn. \"I knew that.\" She dries the cricket bat with a dishtowel. \"I just assumed he'd died recently, got over the Welsh bint, and come back where he belongs.\" You report that, as of this morning, he was alive and well. \"Pity,\" she says.",
        "choices": [{"goto": 111}]
    },
    111: {
        "text": "\"So, who have I been talking to?\" Mrs Fellaman asks. As you advise her the ghost probably took the form of her husband to suit her, you knock on the wall in front of the missing alcove. Your third knock produces a hollow thud. You cast your eyes around the room and spot Knuckles' discarded masonry hammer. You get a solid two-handed grip and inform Mrs Fellaman that you are about to make a mess. \"Wait a minute,\" she says. You swing the hammer. The iron head goes through on the first blow. \"He did look like my Victor. How would he know?\" You knock out the loose plaster around the edges of the hole and use your phone as a torch to peer inside. There is a strong flash of carbolic soap and fish guts, the smell of sweat, and a blast of cold that numbs your fingers. Vestigia! The torch beam casts shadows around a hollow that you quickly recognise as the eye socket of a skull. Squinting, you see what might be a pile of other bones beneath it-the rest of the skeleton. \"What can you see?\" You look at Mrs Fellaman. Perhaps the body was some mistreated domestic worker from the late 19th century. Then again, Eugenia Fellaman has quite a temper. Perhaps there was somebody after her beloved Victor who never made it out of the flat. Nine times out of ten, when the bones are removed, the ghost goes with them. You can always borrow Ernie again and take a stroll along Prince of Wales Road, just to check. For now, though, you have a phone call to make. What happens afterwards will not be your problem. Well done, you've completed your first case file. Welcome to Rivers of London: the Roleplaying Game! THE END.",
        "choices": []
    },
    999: {"text": "Suas forças se esvaem. Você cai no chão, incapaz de continuar. A escuridão toma conta de sua visão. Sua jornada termina aqui.", "choices": []}
}