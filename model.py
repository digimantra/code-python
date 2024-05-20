import os
import librosa
import numpy as np
from librosa import feature
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Set up the directory paths for different sound classes
sound_classes_path = [
    'C:\\AI_ML_Models\\data\\A capella',
'C:\\AI_ML_Models\\data\\Accelerating, revving, vroom',
'C:\\AI_ML_Models\\data\\Accordion',
'C:\\AI_ML_Models\\data\\Acoustic guitar',
'C:\\AI_ML_Models\\data\\Afrobeat',
'C:\\AI_ML_Models\\data\\Air brake',
'C:\\AI_ML_Models\\data\\Air conditioning',
'C:\\AI_ML_Models\\data\\Air horn, truck horn',
'C:\\AI_ML_Models\\data\\Aircraft',
'C:\\AI_ML_Models\\data\\Aircraft engine',
'C:\\AI_ML_Models\\data\\Alarm',
'C:\\AI_ML_Models\\data\\Alarm clock',
'C:\\AI_ML_Models\\data\\Ambient music',
'C:\\AI_ML_Models\\data\\Ambulance (siren)',
'C:\\AI_ML_Models\\data\\Angry music',
'C:\\AI_ML_Models\\data\\Animal',
'C:\\AI_ML_Models\\data\\Applause',
'C:\\AI_ML_Models\\data\\Arrow',
'C:\\AI_ML_Models\\data\\Artillery fire',
'C:\\AI_ML_Models\\data\\Babbling',
'C:\\AI_ML_Models\\data\\Baby cry, infant cry',
'C:\\AI_ML_Models\\data\\Baby laughter',
'C:\\AI_ML_Models\\data\\Background music',
'C:\\AI_ML_Models\\data\\Bagpipes',
'C:\\AI_ML_Models\\data\\Bang',
'C:\\AI_ML_Models\\data\\Banjo',
'C:\\AI_ML_Models\\data\\Bark',
'C:\\AI_ML_Models\\data\\Basketball bounce',
'C:\\AI_ML_Models\\data\\Bass drum',
'C:\\AI_ML_Models\\data\\Bass guitar',
'C:\\AI_ML_Models\\data\\Bathtub (filling or washing)',
'C:\\AI_ML_Models\\data\\Beatboxing',
'C:\\AI_ML_Models\\data\\Bee, wasp, etc',
'C:\\AI_ML_Models\\data\\Beep, bleep',
'C:\\AI_ML_Models\\data\\Bell',
'C:\\AI_ML_Models\\data\\Bellow',
'C:\\AI_ML_Models\\data\\Belly laugh',
'C:\\AI_ML_Models\\data\\Bicycle',
'C:\\AI_ML_Models\\data\\Bicycle bell',
'C:\\AI_ML_Models\\data\\Bird',
'C:\\AI_ML_Models\\data\\Bird flight, flapping wings',
'C:\\AI_ML_Models\\data\\Bird vocalization, bird call, bird song',
'C:\\AI_ML_Models\\data\\Biting',
'C:\\AI_ML_Models\\data\\Bleat',
'C:\\AI_ML_Models\\data\\Blender',
'C:\\AI_ML_Models\\data\\Bluegrass',
'C:\\AI_ML_Models\\data\\Blues',
'C:\\AI_ML_Models\\data\\Boat, Water vehicle',
'C:\\AI_ML_Models\\data\\Boiling',
'C:\\AI_ML_Models\\data\\Boing',
'C:\\AI_ML_Models\\data\\Boom',
'C:\\AI_ML_Models\\data\\Bouncing',
'C:\\AI_ML_Models\\data\\Bow-wow',
'C:\\AI_ML_Models\\data\\Bowed string instrument',
'C:\\AI_ML_Models\\data\\Brass instrument',
'C:\\AI_ML_Models\\data\\Breaking',
'C:\\AI_ML_Models\\data\\Breathing',
'C:\\AI_ML_Models\\data\\Burping, eructation',
'C:\\AI_ML_Models\\data\\Burst, pop',
'C:\\AI_ML_Models\\data\\Bus',
'C:\\AI_ML_Models\\data\\Busy signal',
'C:\\AI_ML_Models\\data\\Buzz',
'C:\\AI_ML_Models\\data\\Buzzer',
'C:\\AI_ML_Models\\data\\Cacophony',
'C:\\AI_ML_Models\\data\\Camera',
'C:\\AI_ML_Models\\data\\Canidae, dogs, wolves',
'C:\\AI_ML_Models\\data\\Cap gun',
'C:\\AI_ML_Models\\data\\Car',
'C:\\AI_ML_Models\\data\\Car alarm',
'C:\\AI_ML_Models\\data\\Car passing by',
'C:\\AI_ML_Models\\data\\Carnatic music',
'C:\\AI_ML_Models\\data\\Cash register',
'C:\\AI_ML_Models\\data\\Cat',
'C:\\AI_ML_Models\\data\\Caterwaul',
'C:\\AI_ML_Models\\data\\Caw',
'C:\\AI_ML_Models\\data\\Cello',
'C:\\AI_ML_Models\\data\\Chainsaw',
'C:\\AI_ML_Models\\data\\Change ringing (campanology)',
'C:\\AI_ML_Models\\data\\Chant',
'C:\\AI_ML_Models\\data\\Chatter',
'C:\\AI_ML_Models\\data\\Cheering',
'C:\\AI_ML_Models\\data\\Chewing, mastication',
'C:\\AI_ML_Models\\data\\Chicken, rooster',
'C:\\AI_ML_Models\\data\\Child singing',
'C:\\AI_ML_Models\\data\\Child speech, kid speaking',
'C:\\AI_ML_Models\\data\\Children playing',
'C:\\AI_ML_Models\\data\\Chime',
'C:\\AI_ML_Models\\data\\Chink, clink',
'C:\\AI_ML_Models\\data\\Chirp tone',
'C:\\AI_ML_Models\\data\\Chirp, tweet',
'C:\\AI_ML_Models\\data\\Choir',
'C:\\AI_ML_Models\\data\\Chop',
'C:\\AI_ML_Models\\data\\Chopping (food)',
'C:\\AI_ML_Models\\data\\Chorus effect',
'C:\\AI_ML_Models\\data\\Christian music',
'C:\\AI_ML_Models\\data\\Christmas music',
'C:\\AI_ML_Models\\data\\Chuckle, chortle',
'C:\\AI_ML_Models\\data\\Church bell',
'C:\\AI_ML_Models\\data\\Civil defense siren',
'C:\\AI_ML_Models\\data\\Clang',
'C:\\AI_ML_Models\\data\\Clapping',
'C:\\AI_ML_Models\\data\\Clarinet',
'C:\\AI_ML_Models\\data\\Classical music',
'C:\\AI_ML_Models\\data\\Clatter',
'C:\\AI_ML_Models\\data\\Clickety-clack',
'C:\\AI_ML_Models\\data\\Clicking',
'C:\\AI_ML_Models\\data\\Clip-clop',
'C:\\AI_ML_Models\\data\\Clock',
'C:\\AI_ML_Models\\data\\Cluck',
'C:\\AI_ML_Models\\data\\Coin (dropping)',
'C:\\AI_ML_Models\\data\\Computer keyboard',
'C:\\AI_ML_Models\\data\\Conversation',
'C:\\AI_ML_Models\\data\\Coo',
'C:\\AI_ML_Models\\data\\Cough',
'C:\\AI_ML_Models\\data\\Country',
'C:\\AI_ML_Models\\data\\Cowbell',
'C:\\AI_ML_Models\\data\\Crack',
'C:\\AI_ML_Models\\data\\Crackle',
'C:\\AI_ML_Models\\data\\Creak',
'C:\\AI_ML_Models\\data\\Crow',
'C:\\AI_ML_Models\\data\\Crowd',
'C:\\AI_ML_Models\\data\\Crowing, cock-a-doodle-doo',
'C:\\AI_ML_Models\\data\\Crumpling, crinkling',
'C:\\AI_ML_Models\\data\\Crunch',
'C:\\AI_ML_Models\\data\\Crushing',
'C:\\AI_ML_Models\\data\\Crying, sobbing',
'C:\\AI_ML_Models\\data\\Cupboard open or close',
'C:\\AI_ML_Models\\data\\Cutlery, silverware',
'C:\\AI_ML_Models\\data\\Cymbal',
'C:\\AI_ML_Models\\data\\Dance music',
'C:\\AI_ML_Models\\data\\Dental drill',
'C:\\AI_ML_Models\\data\\Dial tone',
'C:\\AI_ML_Models\\data\\Didgeridoo',
'C:\\AI_ML_Models\\data\\Ding',
'C:\\AI_ML_Models\\data\\Ding-dong',
'C:\\AI_ML_Models\\data\\Disco',
'C:\\AI_ML_Models\\data\\Dishes, pots, and pans',
'C:\\AI_ML_Models\\data\\Distortion',
'C:\\AI_ML_Models\\data\\Dog',
'C:\\AI_ML_Models\\data\\Domestic animals, pets',
'C:\\AI_ML_Models\\data\\Door',
'C:\\AI_ML_Models\\data\\Doorbell',
'C:\\AI_ML_Models\\data\\Double bass',
'C:\\AI_ML_Models\\data\\Drawer open or close',
'C:\\AI_ML_Models\\data\\Drill',
'C:\\AI_ML_Models\\data\\Drip',
'C:\\AI_ML_Models\\data\\Drum',
'C:\\AI_ML_Models\\data\\Drum and bass',
'C:\\AI_ML_Models\\data\\Drum kit',
'C:\\AI_ML_Models\\data\\Drum machine',
'C:\\AI_ML_Models\\data\\Drum roll',
'C:\\AI_ML_Models\\data\\Dubstep',
'C:\\AI_ML_Models\\data\\Duck',
'C:\\AI_ML_Models\\data\\Echo',
'C:\\AI_ML_Models\\data\\Effects unit',
'C:\\AI_ML_Models\\data\\Electric guitar',
'C:\\AI_ML_Models\\data\\Electric piano',
'C:\\AI_ML_Models\\data\\Electric shaver, electric razor',
'C:\\AI_ML_Models\\data\\Electric toothbrush',
'C:\\AI_ML_Models\\data\\Electronic dance music',
'C:\\AI_ML_Models\\data\\Electronic music',
'C:\\AI_ML_Models\\data\\Electronic organ',
'C:\\AI_ML_Models\\data\\Electronic tuner',
'C:\\AI_ML_Models\\data\\Electronica',
'C:\\AI_ML_Models\\data\\Emergency vehicle',
'C:\\AI_ML_Models\\data\\Engine',
'C:\\AI_ML_Models\\data\\Engine knocking',
'C:\\AI_ML_Models\\data\\Engine starting',
'C:\\AI_ML_Models\\data\\Environmental noise',
'C:\\AI_ML_Models\\data\\Eruption',
'C:\\AI_ML_Models\\data\\Exciting music',
'C:\\AI_ML_Models\\data\\Explosion',
'C:\\AI_ML_Models\\data\\Fart',
'C:\\AI_ML_Models\\data\\Female singing',
'C:\\AI_ML_Models\\data\\Female speech, woman speaking',
'C:\\AI_ML_Models\\data\\Field recording',
'C:\\AI_ML_Models\\data\\Filing (rasp)',
'C:\\AI_ML_Models\\data\\Fill (with liquid)',
'C:\\AI_ML_Models\\data\\Finger snapping',
'C:\\AI_ML_Models\\data\\Fire',
'C:\\AI_ML_Models\\data\\Fire alarm',
'C:\\AI_ML_Models\\data\\Fire engine, fire truck (siren)',
'C:\\AI_ML_Models\\data\\Firecracker',
'C:\\AI_ML_Models\\data\\Fireworks',
'C:\\AI_ML_Models\\data\\Fixed-wing aircraft, airplane',
'C:\\AI_ML_Models\\data\\Flamenco',
'C:\\AI_ML_Models\\data\\Flap',
'C:\\AI_ML_Models\\data\\Flute',
'C:\\AI_ML_Models\\data\\Foghorn',
'C:\\AI_ML_Models\\data\\Folk music',
'C:\\AI_ML_Models\\data\\Fowl',
'C:\\AI_ML_Models\\data\\French horn',
'C:\\AI_ML_Models\\data\\Frog',
'C:\\AI_ML_Models\\data\\Frying (food)',
'C:\\AI_ML_Models\\data\\Funk',
'C:\\AI_ML_Models\\data\\Funny music',
'C:\\AI_ML_Models\\data\\Fusillade',
'C:\\AI_ML_Models\\data\\Gargling',
'C:\\AI_ML_Models\\data\\Gasp',
'C:\\AI_ML_Models\\data\\Gears',
'C:\\AI_ML_Models\\data\\Giggle',
'C:\\AI_ML_Models\\data\\Glass',
'C:\\AI_ML_Models\\data\\Glockenspiel',
'C:\\AI_ML_Models\\data\\Goat',
'C:\\AI_ML_Models\\data\\Gobble',
'C:\\AI_ML_Models\\data\\Gong',
'C:\\AI_ML_Models\\data\\Goose',
'C:\\AI_ML_Models\\data\\Gospel music',
'C:\\AI_ML_Models\\data\\Groan',
'C:\\AI_ML_Models\\data\\Growling',
'C:\\AI_ML_Models\\data\\Grunge',
'C:\\AI_ML_Models\\data\\Grunt',
'C:\\AI_ML_Models\\data\\Guitar',
'C:\\AI_ML_Models\\data\\Gunshot, gunfire',
'C:\\AI_ML_Models\\data\\Gurgling',
'C:\\AI_ML_Models\\data\\Gush',
'C:\\AI_ML_Models\\data\\Hair dryer',
'C:\\AI_ML_Models\\data\\Hammer',
'C:\\AI_ML_Models\\data\\Hammond organ',
'C:\\AI_ML_Models\\data\\Hands',
'C:\\AI_ML_Models\\data\\Harmonic',
'C:\\AI_ML_Models\\data\\Harmonica',
'C:\\AI_ML_Models\\data\\Harp',
'C:\\AI_ML_Models\\data\\Harpsichord',
'C:\\AI_ML_Models\\data\\Heart murmur',
'C:\\AI_ML_Models\\data\\Heart sounds, heartbeat',
'C:\\AI_ML_Models\\data\\Heavy engine (low frequency)',
'C:\\AI_ML_Models\\data\\Heavy metal',
'C:\\AI_ML_Models\\data\\Helicopter',
'C:\\AI_ML_Models\\data\\Hi-hat',
'C:\\AI_ML_Models\\data\\Hiccup',
'C:\\AI_ML_Models\\data\\Hip hop music',
'C:\\AI_ML_Models\\data\\Hiss',
'C:\\AI_ML_Models\\data\\Honk',
'C:\\AI_ML_Models\\data\\Hoot',
'C:\\AI_ML_Models\\data\\Horse',
'C:\\AI_ML_Models\\data\\House music',
'C:\\AI_ML_Models\\data\\Howl',
'C:\\AI_ML_Models\\data\\Hubbub, speech noise, speech babble',
'C:\\AI_ML_Models\\data\\Hum',
'C:\\AI_ML_Models\\data\\Humming',
'C:\\AI_ML_Models\\data\\Ice cream truck, ice cream van',
'C:\\AI_ML_Models\\data\\Idling',
'C:\\AI_ML_Models\\data\\Independent music',
'C:\\AI_ML_Models\\data\\Insect',
'C:\\AI_ML_Models\\data\\Inside, large room or hall',
'C:\\AI_ML_Models\\data\\Inside, public space',
'C:\\AI_ML_Models\\data\\Inside, small room',
'C:\\AI_ML_Models\\data\\Jackhammer',
'C:\\AI_ML_Models\\data\\Jazz',
'C:\\AI_ML_Models\\data\\Jet engine',
'C:\\AI_ML_Models\\data\\Jingle (music)',
'C:\\AI_ML_Models\\data\\Jingle bell',
'C:\\AI_ML_Models\\data\\Jingle, tinkle',
'C:\\AI_ML_Models\\data\\Keyboard (musical)',
'C:\\AI_ML_Models\\data\\Keys jangling',
'C:\\AI_ML_Models\\data\\Knock',
'C:\\AI_ML_Models\\data\\Laughter',
'C:\\AI_ML_Models\\data\\Lawn mower',
'C:\\AI_ML_Models\\data\\Light engine (high frequency)',
'C:\\AI_ML_Models\\data\\Liquid',
'C:\\AI_ML_Models\\data\\Livestock, farm animals, working animals',
'C:\\AI_ML_Models\\data\\Lullaby',
'C:\\AI_ML_Models\\data\\Machine gun',
'C:\\AI_ML_Models\\data\\Mains hum',
'C:\\AI_ML_Models\\data\\Male singing',
'C:\\AI_ML_Models\\data\\Male speech, man speaking',
'C:\\AI_ML_Models\\data\\Mallet percussion',
'C:\\AI_ML_Models\\data\\Mandolin',
'C:\\AI_ML_Models\\data\\Mantra',
'C:\\AI_ML_Models\\data\\Maraca',
'C:\\AI_ML_Models\\data\\Marimba, xylophone',
'C:\\AI_ML_Models\\data\\Mechanical fan',
'C:\\AI_ML_Models\\data\\Mechanisms',
'C:\\AI_ML_Models\\data\\Medium engine (mid frequency)',
'C:\\AI_ML_Models\\data\\Meow',
'C:\\AI_ML_Models\\data\\Microwave oven',
'C:\\AI_ML_Models\\data\\Middle Eastern music',
'C:\\AI_ML_Models\\data\\Motor vehicle (road)',
'C:\\AI_ML_Models\\data\\Motorboat, speedboat',
'C:\\AI_ML_Models\\data\\Motorcycle',
'C:\\AI_ML_Models\\data\\Mouse',
'C:\\AI_ML_Models\\data\\Music for children',
'C:\\AI_ML_Models\\data\\Music of Africa',
'C:\\AI_ML_Models\\data\\Music of Asia',
'C:\\AI_ML_Models\\data\\Music of Bollywood',
'C:\\AI_ML_Models\\data\\Music of Latin America',
'C:\\AI_ML_Models\\data\\Musical instrument',
'C:\\AI_ML_Models\\data\\Narration, monologue',
'C:\\AI_ML_Models\\data\\Neigh, whinny',
'C:\\AI_ML_Models\\data\\New-age music',
'C:\\AI_ML_Models\\data\\Noise',
'C:\\AI_ML_Models\\data\\Ocean',
'C:\\AI_ML_Models\\data\\Oink',
'C:\\AI_ML_Models\\data\\Opera',
'C:\\AI_ML_Models\\data\\Orchestra',
'C:\\AI_ML_Models\\data\\Organ',
'C:\\AI_ML_Models\\data\\Outside, rural or natural',
'C:\\AI_ML_Models\\data\\Outside, urban or manmade',
'C:\\AI_ML_Models\\data\\Owl',
'C:\\AI_ML_Models\\data\\Pant',
'C:\\AI_ML_Models\\data\\Patter',
'C:\\AI_ML_Models\\data\\Percussion',
'C:\\AI_ML_Models\\data\\Piano',
'C:\\AI_ML_Models\\data\\Pig',
'C:\\AI_ML_Models\\data\\Pigeon, dove',
'C:\\AI_ML_Models\\data\\Ping',
'C:\\AI_ML_Models\\data\\Pink noise',
'C:\\AI_ML_Models\\data\\Pizzicato',
'C:\\AI_ML_Models\\data\\Plop',
'C:\\AI_ML_Models\\data\\Plucked string instrument',
'C:\\AI_ML_Models\\data\\Police car (siren)',
'C:\\AI_ML_Models\\data\\Pop music',
'C:\\AI_ML_Models\\data\\Pour',
'C:\\AI_ML_Models\\data\\Power tool',
'C:\\AI_ML_Models\\data\\Power windows, electric windows',
'C:\\AI_ML_Models\\data\\Printer',
'C:\\AI_ML_Models\\data\\Progressive rock',
'C:\\AI_ML_Models\\data\\Propeller, airscrew',
'C:\\AI_ML_Models\\data\\Psychedelic rock',
'C:\\AI_ML_Models\\data\\Pulleys',
'C:\\AI_ML_Models\\data\\Pulse',
'C:\\AI_ML_Models\\data\\Pump (liquid)',
'C:\\AI_ML_Models\\data\\Punk rock',
'C:\\AI_ML_Models\\data\\Purr',
'C:\\AI_ML_Models\\data\\Quack',
'C:\\AI_ML_Models\\data\\Race car, auto racing',
'C:\\AI_ML_Models\\data\\Radio',
'C:\\AI_ML_Models\\data\\Rail transport',
'C:\\AI_ML_Models\\data\\Railroad car, train wagon',
'C:\\AI_ML_Models\\data\\Rain',
'C:\\AI_ML_Models\\data\\Rain on surface',
'C:\\AI_ML_Models\\data\\Raindrop',
'C:\\AI_ML_Models\\data\\Rapping',
'C:\\AI_ML_Models\\data\\Rattle',
'C:\\AI_ML_Models\\data\\Rattle (instrument)',
'C:\\AI_ML_Models\\data\\Reggae',
'C:\\AI_ML_Models\\data\\Reverberation',
'C:\\AI_ML_Models\\data\\Reversing beeps',
'C:\\AI_ML_Models\\data\\Rhythm and blues',
'C:\\AI_ML_Models\\data\\Rimshot',
'C:\\AI_ML_Models\\data\\Ringtone',
'C:\\AI_ML_Models\\data\\Roar',
'C:\\AI_ML_Models\\data\\Roaring cats (lions, tigers)',
'C:\\AI_ML_Models\\data\\Rock and roll',
'C:\\AI_ML_Models\\data\\Rock music',
'C:\\AI_ML_Models\\data\\Rodents, rats, mice',
'C:\\AI_ML_Models\\data\\Roll',
'C:\\AI_ML_Models\\data\\Rowboat, canoe, kayak',
'C:\\AI_ML_Models\\data\\Rub',
'C:\\AI_ML_Models\\data\\Rumble',
'C:\\AI_ML_Models\\data\\Run',
'C:\\AI_ML_Models\\data\\Rustle',
'C:\\AI_ML_Models\\data\\Rustling leaves',
'C:\\AI_ML_Models\\data\\Sailboat, sailing ship',
'C:\\AI_ML_Models\\data\\Salsa music',
'C:\\AI_ML_Models\\data\\Sampler',
'C:\\AI_ML_Models\\data\\Sanding',
'C:\\AI_ML_Models\\data\\Sawing',
'C:\\AI_ML_Models\\data\\Saxophone',
'C:\\AI_ML_Models\\data\\Scary music',
'C:\\AI_ML_Models\\data\\Scissors',
'C:\\AI_ML_Models\\data\\Scrape',
'C:\\AI_ML_Models\\data\\Scratch',
'C:\\AI_ML_Models\\data\\Scratching (performance technique)',
'C:\\AI_ML_Models\\data\\Screaming',
'C:\\AI_ML_Models\\data\\Sewing machine',
'C:\\AI_ML_Models\\data\\Shatter',
'C:\\AI_ML_Models\\data\\Sheep',
'C:\\AI_ML_Models\\data\\Ship',
'C:\\AI_ML_Models\\data\\Shout',
'C:\\AI_ML_Models\\data\\Shuffle',
'C:\\AI_ML_Models\\data\\Shuffling cards',
'C:\\AI_ML_Models\\data\\Sidetone',
'C:\\AI_ML_Models\\data\\Sigh',
'C:\\AI_ML_Models\\data\\Silence',
'C:\\AI_ML_Models\\data\\Sine wave',
'C:\\AI_ML_Models\\data\\Singing',
'C:\\AI_ML_Models\\data\\Singing bowl',
'C:\\AI_ML_Models\\data\\Single-lens reflex camera',
'C:\\AI_ML_Models\\data\\Sink (filling or washing)',
'C:\\AI_ML_Models\\data\\Siren',
'C:\\AI_ML_Models\\data\\Sitar',
'C:\\AI_ML_Models\\data\\Sizzle',
'C:\\AI_ML_Models\\data\\Ska',
'C:\\AI_ML_Models\\data\\Skateboard',
'C:\\AI_ML_Models\\data\\Skidding',
'C:\\AI_ML_Models\\data\\Slam',
'C:\\AI_ML_Models\\data\\Slap, smack',
'C:\\AI_ML_Models\\data\\Sliding door',
'C:\\AI_ML_Models\\data\\Slosh',
'C:\\AI_ML_Models\\data\\Smash, crash',
'C:\\AI_ML_Models\\data\\Smoke detector, smoke alarm',
'C:\\AI_ML_Models\\data\\Snake',
'C:\\AI_ML_Models\\data\\Snare drum',
'C:\\AI_ML_Models\\data\\Sneeze',
'C:\\AI_ML_Models\\data\\Snicker',
'C:\\AI_ML_Models\\data\\Sniff',
'C:\\AI_ML_Models\\data\\Snoring',
'C:\\AI_ML_Models\\data\\Snort',
'C:\\AI_ML_Models\\data\\Sonar',
'C:\\AI_ML_Models\\data\\Song',
'C:\\AI_ML_Models\\data\\Soul music',
'C:\\AI_ML_Models\\data\\Sound effect',
'C:\\AI_ML_Models\\data\\Soundtrack music',
'C:\\AI_ML_Models\\data\\Speech synthesizer',
'C:\\AI_ML_Models\\data\\Splash, splatter',
'C:\\AI_ML_Models\\data\\Splinter',
'C:\\AI_ML_Models\\data\\Spray',
'C:\\AI_ML_Models\\data\\Squawk',
'C:\\AI_ML_Models\\data\\Squeak',
'C:\\AI_ML_Models\\data\\Squeal',
'C:\\AI_ML_Models\\data\\Squish',
'C:\\AI_ML_Models\\data\\Static',
'C:\\AI_ML_Models\\data\\Steam',
'C:\\AI_ML_Models\\data\\Steam whistle',
'C:\\AI_ML_Models\\data\\Steelpan',
'C:\\AI_ML_Models\\data\\Stir',
'C:\\AI_ML_Models\\data\\Stomach rumble',
'C:\\AI_ML_Models\\data\\Stream',
'C:\\AI_ML_Models\\data\\String section',
'C:\\AI_ML_Models\\data\\Strum',
'C:\\AI_ML_Models\\data\\Subway, metro, underground',
'C:\\AI_ML_Models\\data\\Swing music',
'C:\\AI_ML_Models\\data\\Synthesizer',
'C:\\AI_ML_Models\\data\\Synthetic singing',
'C:\\AI_ML_Models\\data\\Tabla',
'C:\\AI_ML_Models\\data\\Tambourine',
'C:\\AI_ML_Models\\data\\Tap',
'C:\\AI_ML_Models\\data\\Tapping (guitar technique)',
'C:\\AI_ML_Models\\data\\Tearing',
'C:\\AI_ML_Models\\data\\Techno',
'C:\\AI_ML_Models\\data\\Telephone',
'C:\\AI_ML_Models\\data\\Telephone bell ringing',
'C:\\AI_ML_Models\\data\\Telephone dialing, DTMF',
'C:\\AI_ML_Models\\data\\Television',
'C:\\AI_ML_Models\\data\\Tender music',
'C:\\AI_ML_Models\\data\\Theme music',
'C:\\AI_ML_Models\\data\\Theremin',
'C:\\AI_ML_Models\\data\\Throat clearing',
'C:\\AI_ML_Models\\data\\Throbbing',
'C:\\AI_ML_Models\\data\\Thump, thud',
'C:\\AI_ML_Models\\data\\Thunder',
'C:\\AI_ML_Models\\data\\Thunderstorm',
'C:\\AI_ML_Models\\data\\Thunk',
'C:\\AI_ML_Models\\data\\Tick',
'C:\\AI_ML_Models\\data\\Tick-tock',
'C:\\AI_ML_Models\\data\\Timpani',
'C:\\AI_ML_Models\\data\\Tire squeal',
'C:\\AI_ML_Models\\data\\Toilet flush',
'C:\\AI_ML_Models\\data\\Tools',
'C:\\AI_ML_Models\\data\\Toot',
'C:\\AI_ML_Models\\data\\Toothbrush',
'C:\\AI_ML_Models\\data\\Traditional music',
'C:\\AI_ML_Models\\data\\Traffic noise, roadway noise',
'C:\\AI_ML_Models\\data\\Train',
'C:\\AI_ML_Models\\data\\Train horn',
'C:\\AI_ML_Models\\data\\Train wheels squealing',
'C:\\AI_ML_Models\\data\\Train whistle',
'C:\\AI_ML_Models\\data\\Trance music',
'C:\\AI_ML_Models\\data\\Trickle, dribble',
'C:\\AI_ML_Models\\data\\Trombone',
'C:\\AI_ML_Models\\data\\Truck',
'C:\\AI_ML_Models\\data\\Trumpet',
'C:\\AI_ML_Models\\data\\Tubular bells',
'C:\\AI_ML_Models\\data\\Tuning fork',
'C:\\AI_ML_Models\\data\\Turkey',
'C:\\AI_ML_Models\\data\\Typewriter',
'C:\\AI_ML_Models\\data\\Typing',
'C:\\AI_ML_Models\\data\\Vacuum cleaner',
'C:\\AI_ML_Models\\data\\Vehicle',
'C:\\AI_ML_Models\\data\\Vehicle horn, car horn, honking',
'C:\\AI_ML_Models\\data\\Vibraphone',
'C:\\AI_ML_Models\\data\\Vibration',
'C:\\AI_ML_Models\\data\\Video game music',
'C:\\AI_ML_Models\\data\\Violin, fiddle',
'C:\\AI_ML_Models\\data\\Vocal music',
'C:\\AI_ML_Models\\data\\Wail, moan',
'C:\\AI_ML_Models\\data\\Walk, footsteps',
'C:\\AI_ML_Models\\data\\Water',
'C:\\AI_ML_Models\\data\\Water tap, faucet',
'C:\\AI_ML_Models\\data\\Waterfall',
'C:\\AI_ML_Models\\data\\Waves, surf',
'C:\\AI_ML_Models\\data\\Wedding music',
'C:\\AI_ML_Models\\data\\Whack, thwack',
'C:\\AI_ML_Models\\data\\Whale vocalization',
'C:\\AI_ML_Models\\data\\Wheeze',
'C:\\AI_ML_Models\\data\\Whimper',
'C:\\AI_ML_Models\\data\\Whimper (dog)',
'C:\\AI_ML_Models\\data\\Whip',
'C:\\AI_ML_Models\\data\\Whir',
'C:\\AI_ML_Models\\data\\Whispering',
'C:\\AI_ML_Models\\data\\Whistle',
'C:\\AI_ML_Models\\data\\Whistling',
'C:\\AI_ML_Models\\data\\White noise',
'C:\\AI_ML_Models\\data\\Whoop',
'C:\\AI_ML_Models\\data\\Whoosh, swoosh, swish',
'C:\\AI_ML_Models\\data\\Wild animals',
'C:\\AI_ML_Models\\data\\Wind',
'C:\\AI_ML_Models\\data\\Wind chime',
'C:\\AI_ML_Models\\data\\Wind instrument, woodwind instrument',
'C:\\AI_ML_Models\\data\\Wind noise (microphone)',
'C:\\AI_ML_Models\\data\\Wood',
'C:\\AI_ML_Models\\data\\Wood block',
'C:\\AI_ML_Models\\data\\Writing',
'C:\\AI_ML_Models\\data\\Yell',
'C:\\AI_ML_Models\\data\\Yip',
'C:\\AI_ML_Models\\data\\Yodeling',
'C:\\AI_ML_Models\\data\\Zing',
'C:\\AI_ML_Models\\data\\Zipper (clothing)',
'C:\\AI_ML_Models\\data\\Zither',
]

# Initialize empty lists to store audio samples and their corresponding labels
audio_samples = []
labels = []

# Load and preprocess audio files for each class
for class_label, class_path in enumerate(sound_classes_path):
    for filename in os.listdir(class_path):
        if filename.endswith('.mp3') or filename.endswith('.m4a'):
            file_path = os.path.join(class_path, filename)
            audio, _ = librosa.load(file_path, sr=22050, duration=2.5, mono=True)
            spectrogram = feature.melspectrogram(y=audio, sr=22050, n_fft=256, n_mels=128, hop_length=512)
            desired_time_steps = 129

            if spectrogram.shape[1] < desired_time_steps:
                pad_width = desired_time_steps - spectrogram.shape[1]
                pad_width_left = pad_width // 2
                pad_width_right = pad_width - pad_width_left
                spectrogram = np.pad(spectrogram, pad_width=((0, 0), (pad_width_left, pad_width_right)), mode='constant')
            elif spectrogram.shape[1] > desired_time_steps:
                spectrogram = spectrogram[:, :desired_time_steps]

            audio_samples.append(spectrogram.T)
            labels.append(class_label)

# Convert lists to numpy arrays
audio_samples = np.array(audio_samples)
labels = np.array(labels)

# Use LabelEncoder to convert class labels to integers
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels)

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(audio_samples, labels_encoded, test_size=0.20, random_state=42)

# Build the model
num_classes = len(sound_classes_path)
model = Sequential([
    Conv2D(128, (3, 3), activation='relu', input_shape=(X_train.shape[1], X_train.shape[2], 1)),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(num_classes, activation='softmax')
])

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Set up early stopping to prevent overfitting
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# Train the model
history = model.fit(X_train, y_train, epochs=15, batch_size=32, validation_split=0.2, callbacks=[early_stopping])

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print("Test Loss:", loss)
print("Test Accuracy:", accuracy)

# Save the model to disk
model.save("multi_class_audio_model.h5")

# Save the label encoder for later use
np.save("label_encoder.npy", label_encoder.classes_)
