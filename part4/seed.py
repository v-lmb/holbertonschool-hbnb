from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

app = create_app()

with app.app_context():
    db.create_all()

    # --- Users ---
    admin = User.query.filter_by(email='admin@hbnb.io').first()
    if not admin:
        admin = User(first_name='Admin', last_name='HBnB',
                     email='admin@hbnb.io', password='admin1234', is_admin=True)
        db.session.add(admin)
        print('Admin created: admin@hbnb.io / admin1234')

    watson = User.query.filter_by(email='watson@baker.st').first()
    if not watson:
        watson = User(first_name='John', last_name='Watson',
                      email='watson@baker.st', password='watson1234')
        db.session.add(watson)
        print('User created: watson@baker.st / watson1234')

    irene = User.query.filter_by(email='irene@opera.fr').first()
    if not irene:
        irene = User(first_name='Irene', last_name='Adler',
                     email='irene@opera.fr', password='irene1234')
        db.session.add(irene)
        print('User created: irene@opera.fr / irene1234')

    moriarty = User.query.filter_by(email='moriarty@consulting.co').first()
    if not moriarty:
        moriarty = User(first_name='James', last_name='Moriarty',
                        email='moriarty@consulting.co', password='moriarty1234')
        db.session.add(moriarty)
        print('User created: moriarty@consulting.co / moriarty1234')

    ganimard = User.query.filter_by(email='ganimard@prefecture.fr').first()
    if not ganimard:
        ganimard = User(first_name='Inspecteur', last_name='Ganimard',
                        email='ganimard@prefecture.fr', password='ganimard1234')
        db.session.add(ganimard)
        print('User created: ganimard@prefecture.fr / ganimard1234')

    lupin = User.query.filter_by(email='lupin@nowhere.fr').first()
    if not lupin:
        lupin = User(first_name='Arsène', last_name='Lupin',
                     email='lupin@nowhere.fr', password='lupin1234')
        db.session.add(lupin)
        print('User created: lupin@nowhere.fr / lupin1234')

    sherlock = User.query.filter_by(email='holmes@baker.st').first()
    if not sherlock:
        sherlock = User(first_name='Sherlock', last_name='Holmes',
                        email='holmes@baker.st', password='holmes1234')
        db.session.add(sherlock)
        print('User created: holmes@baker.st / holmes1234')

    db.session.flush()

    # --- Amenities ---
    amenity_names = ['WiFi', 'Swimming Pool', 'Parking/Carriage House', 'Air conditioning',
                     'Fitted kitchen', 'Fireplace', 'Library', 'Wine Cellar', 'Stables', 'Gas Lighting']
    amenities = {}
    for name in amenity_names:
        a = Amenity.query.filter_by(name=name).first()
        if not a:
            a = Amenity(name=name)
            db.session.add(a)
            print(f'Amenity created: {name}')
        amenities[name] = a

    db.session.flush()

    # --- Places ---
    place1 = Place.query.filter_by(title='221B Baker Street').first()
    if not place1:
        place1 = Place(
            title='221B Baker Street',
            description='A legendary first-floor flat in the heart of London, '
                        'just off Baker Street. The sitting room features two armchairs '
                        'by the fireplace, a cluttered writing desk, and a persistent '
                        'smell of tobacco. The library wall is lined with case files, '
                        'monographs on obscure subjects, and at least one loaded revolver '
                        'somewhere among the shelves — location unknown. '
                        'The landlady, Mrs Hudson, provides breakfast but declines all '
                        'responsibility for bullet holes in the walls. '
                        'Ideal for analytical minds, light sleepers, and those '
                        'who do not object to the occasional violin at 3 a.m.',
            price=50.0,
            latitude=51.5237,
            longitude=-0.1585,
            owner_id=watson.id
        )
        place1.amenities = [amenities['WiFi'], amenities['Fitted kitchen'],
                            amenities['Fireplace'], amenities['Gas Lighting'], amenities['Library']]
        db.session.add(place1)
        print('Place created: 221B Baker Street')

    place2 = Place.query.filter_by(title="Aiguille Creuse Manor").first()
    if not place2:
        place2 = Place(
            title="Aiguille Creuse Manor",
            description='A grand and mysterious manor perched above the chalk cliffs '
                        'of Étretat, overlooking the Channel. The estate features '
                        'a vaulted wine cellar, a well-stocked library of French literature, '
                        'and a swimming pool that appears on no architectural plan. '
                        'Several guests have reported finding hidden passages behind '
                        'the bookshelves — the management neither confirms nor denies this. '
                        'Local legend holds that a certain gentleman thief once used '
                        'the hollow needle nearby as a personal treasury. '
                        'The view at sunset is unrivalled. Valuables should be kept '
                        'in the safe. The combination has already been changed twice this season.',
            price=95.0,
            latitude=49.7436,
            longitude=0.2000,
            owner_id=irene.id
        )
        place2.amenities = [amenities['WiFi'], amenities['Swimming Pool'],
                            amenities['Parking/Carriage House'], amenities['Fitted kitchen'],
                            amenities['Fireplace'], amenities['Wine Cellar'], amenities['Library']]
        db.session.add(place2)
        print("Place created: Aiguille Creuse Manor")

    place4 = Place.query.filter_by(title="The Spider's Web, Pall Mall").first()
    if not place4:
        place4 = Place(
            title="The Spider's Web, Pall Mall",
            description='An impeccably maintained townhouse on Pall Mall, '
                        'steps from the Reform Club and the heart of London\'s power. '
                        'The interiors are quietly opulent: a working fireplace in every room, '
                        'floor-to-ceiling bookshelves in the study, and gas lighting '
                        'that casts the corridors in a permanent amber dusk. '
                        'The kitchen is fully equipped, the staff discreet, '
                        'and the air conditioning was installed at considerable expense '
                        'by a tenant who preferred not to sweat during interrogations. '
                        'Every visitor is observed. Every conversation is noted. '
                        'Correspondence addressed to "The Professor" will be forwarded '
                        'without question. The professor is not in — or so he says.',
            price=200.0,
            latitude=51.5074,
            longitude=-0.1347,
            owner_id=moriarty.id
        )
        place4.amenities = [amenities['WiFi'], amenities['Fitted kitchen'],
                            amenities['Air conditioning'], amenities['Fireplace'],
                            amenities['Library'], amenities['Gas Lighting']]
        db.session.add(place4)
        print("Place created: The Spider's Web, Pall Mall")

    place5 = Place.query.filter_by(title='Villa Cagliostro').first()
    if not place5:
        place5 = Place(
            title='Villa Cagliostro',
            description='A luminous and generously appointed villa on the heights above Monaco, '
                        'with a terrace that overlooks the Mediterranean. '
                        'The infinity pool is heated year-round, the gardens are immaculate, '
                        'and the garage accommodates up to three vehicles — '
                        'no questions asked about registration plates. '
                        'The villa comes fully air-conditioned and stocked with '
                        'a selection of local wines. Previous guests have reported '
                        'missing jewellery, a misplaced Fabergé egg, and on one occasion '
                        'an entire safe that had been relocated to an unknown address. '
                        'The owner denies all involvement and is extraordinarily charming about it. '
                        'A signed disclaimer is required upon check-in.',
            price=150.0,
            latitude=43.7384,
            longitude=7.4246,
            owner_id=lupin.id
        )
        place5.amenities = [amenities['WiFi'], amenities['Swimming Pool'],
                            amenities['Parking/Carriage House'], amenities['Air conditioning']]
        db.session.add(place5)
        print('Place created: Villa Cagliostro')

    place6 = Place.query.filter_by(title='Manoir de Gueures').first()
    if not place6:
        place6 = Place(
            title='Manoir de Gueures',
            description='A secluded 18th-century manor set deep in the Normandy bocage, '
                        'surrounded by orchards and accessible only by a single unpaved lane. '
                        'The estate includes a stone fireplace large enough to stand in, '
                        'a wine cellar with an admirable stock of Calvados, '
                        'and stables that have been recently — and very professionally — renovated. '
                        'The fitted kitchen retains its original oak beams. '
                        'Secret passages are rumoured in every wing and have never been '
                        'officially confirmed, though three separate guests have arrived '
                        'at breakfast from a room they did not go to sleep in. '
                        'The owner requests that guests do not attempt to locate '
                        'the north cellar. Ideal for those who value discretion above all else.',
            price=85.0,
            latitude=49.8710,
            longitude=0.9560,
            owner_id=lupin.id
        )
        place6.amenities = [amenities['WiFi'], amenities['Parking/Carriage House'],
                            amenities['Fitted kitchen'], amenities['Fireplace'],
                            amenities['Wine Cellar'], amenities['Stables']]
        db.session.add(place6)
        print('Place created: Manoir de Gueures')

    place7 = Place.query.filter_by(title='Rue Pergolèse Apartment, Paris').first()
    if not place7:
        place7 = Place(
            title='Rue Pergolèse Apartment, Paris',
            description='A modest but well-kept apartment on the Rue Pergolèse, '
                        'a short walk from the Bois de Boulogne and the Préfecture de Police. '
                        'The rooms are small and functional, lit by gas lamps '
                        'that the owner has never seen fit to replace. '
                        'The kitchen is adequate, the bed is firm, and the walls are thin. '
                        'Neighbours have reported the sound of handcuffs at irregular hours, '
                        'and at least one guest claimed to have seen a wanted poster '
                        'on the back of the bathroom door. '
                        'The inspector is frequently away on assignment and will not be '
                        'available to answer questions. A very reasonable rate for Paris.',
            price=9.0,
            latitude=48.8745,
            longitude=2.2830,
            owner_id=ganimard.id
        )
        place7.amenities = [amenities['WiFi'], amenities['Fitted kitchen'],
                            amenities['Gas Lighting']]
        db.session.add(place7)
        print('Place created: Rue Pergolèse Apartment, Paris')

    place8 = Place.query.filter_by(title='Montague Street Rooms, Bloomsbury').first()
    if not place8:
        place8 = Place(
            title='Montague Street Rooms, Bloomsbury',

            description='A set of first-floor rooms on Montague Street, a short walk '
                        'from the British Museum and the reading room of the British Library. '
                        'These were the first London lodgings of a young consulting detective '
                        'before he was widely known — taken at a reasonable rate, '
                        'kept in a state of organised disorder, '
                        'and vacated abruptly in favour of certain well-known premises nearby. '
                        'The bookshelves retain chemical stains of uncertain origin. '
                        'The gas lighting is original. The desk by the window '
                        'still bears the mark of a scalpel, a compass, and what '
                        'appears to be a monogram burned into the wood. '
                        'Guests who ask too many questions about the previous occupant '
                        'will find the landlady surprisingly forthcoming.',
            price=10.0,
            latitude=51.5194,
            longitude=-0.1270,
            owner_id=sherlock.id
        )
        place8.amenities = [amenities['WiFi'], amenities['Fitted kitchen'],
                            amenities['Fireplace'], amenities['Library'], amenities['Gas Lighting']]
        db.session.add(place8)
        print('Place created: Montague Street Rooms, Bloomsbury')

    place9 = Place.query.filter_by(title='Sussex Downs Cottage').first()
    if not place9:
        place9 = Place(
            title='Sussex Downs Cottage',
            description='A small, austere cottage on the chalk hills of the Sussex Downs, '
                        'half a mile from the nearest village and well beyond the reach '
                        'of the London newspapers. The property includes a south-facing garden, '
                        'a modest library organised by a system comprehensible only to the owner, '
                        'and a working apiary of fifteen hives. '
                        'The kitchen is functional. The fireplace draws well. '
                        'There is no gas lighting — the owner considers it a distraction. '
                        'Guests who arrive unannounced will be observed from the garden '
                        'for approximately four minutes before the door is answered. '
                        'Conversation is welcome; small talk is not. '
                        'The bees are gentle provided you move slowly and think clearly.',
            price=45.0,
            latitude=50.8503,
            longitude=0.1292,
            owner_id=sherlock.id
        )
        place9.amenities = [amenities['WiFi'], amenities['Fitted kitchen'],
                            amenities['Fireplace'], amenities['Library']]
        db.session.add(place9)
        print('Place created: Sussex Downs Cottage')

    db.session.flush()

    # --- Reviews ---
    if not Review.query.filter_by(user_id=irene.id, place_id=place1.id).first():
        db.session.add(Review(
            text='A trusted address. Holmes wasn\'t there, but '
                 'his violin was still lying on the sofa.',
            rating=5,
            user_id=irene.id,
            place_id=place1.id
        ))
        print('Review created: Irene -> 221B Baker Street')

    if not Review.query.filter_by(user_id=watson.id, place_id=place2.id).first():
        db.session.add(Review(
            text='A spellbinding place. I thought I heard footsteps in the hallways '
                 'at night. Holmes would have loved this mystery.',
            rating=4,
            user_id=watson.id,
            place_id=place2.id
        ))
        print("Review created: Watson -> Aiguille Creuse Manor")

    if not Review.query.filter_by(user_id=admin.id, place_id=place2.id).first():
        db.session.add(Review(
            text='The setting is exceptional. It\'s easy to see why Lupin '
                 'kept coming back here.',
            rating=5,
            user_id=admin.id,
            place_id=place2.id
        ))
        print("Review created: Admin -> Aiguille Creuse Manor")

    if not Review.query.filter_by(user_id=ganimard.id, place_id=place4.id).first():
        db.session.add(Review(
            text='I came to arrest the owner. He was not there. '
                 'The WiFi password was "checkmate". I left immediately.',
            rating=2,
            user_id=ganimard.id,
            place_id=place4.id
        ))
        print("Review created: Ganimard -> The Spider's Web")

    if not Review.query.filter_by(user_id=moriarty.id, place_id=place5.id).first():
        db.session.add(Review(
            text='Adequate. Though I suspect the owner read my correspondence. '
                 'The pool is pleasant. I will be back — under a different name.',
            rating=3,
            user_id=moriarty.id,
            place_id=place5.id
        ))
        print('Review created: Moriarty -> Villa Cagliostro')

    if not Review.query.filter_by(user_id=irene.id, place_id=place6.id).first():
        db.session.add(Review(
            text='Charming and remote. I found a hidden door behind the bookcase. '
                 'I left it as I found it — mostly.',
            rating=5,
            user_id=irene.id,
            place_id=place6.id
        ))
        print('Review created: Irene -> Manoir de Gueures')

    if not Review.query.filter_by(user_id=lupin.id, place_id=place7.id).first():
        db.session.add(Review(
            text='A surprisingly comfortable stay. The inspector never noticed I was there. '
                 'Five stars for discretion.',
            rating=5,
            user_id=lupin.id,
            place_id=place7.id
        ))
        print('Review created: Lupin -> Rue Pergolèse Apartment')

    if not Review.query.filter_by(user_id=sherlock.id, place_id=place2.id).first():
        db.session.add(Review(
            text='I spent three days here under an assumed name. The hollow needle '
                 'is visible from the east terrace at low tide. The WiFi password '
                 'was changed four times during my stay. Someone was expecting me.',
            rating=4,
            user_id=sherlock.id,
            place_id=place2.id
        ))
        print('Review created: Sherlock -> Aiguille Creuse Manor')

    if not Review.query.filter_by(user_id=sherlock.id, place_id=place4.id).first():
        db.session.add(Review(
            text='I came in disguise. I left with seventeen pages of notes '
                 'and a confirmed theory. The professor was not present, '
                 'but his influence was in every room. Two stars for the decor. '
                 'Five stars for the evidence.',
            rating=2,
            user_id=sherlock.id,
            place_id=place4.id
        ))
        print("Review created: Sherlock -> The Spider's Web")

    if not Review.query.filter_by(user_id=lupin.id, place_id=place1.id).first():
        db.session.add(Review(
            text='I let myself in through the window on the second floor — '
                 'the latch has been broken for years. A charming flat. '
                 'I left a calling card on the mantelpiece. '
                 'I doubt Holmes noticed until Thursday.',
            rating=4,
            user_id=lupin.id,
            place_id=place1.id
        ))
        print('Review created: Lupin -> 221B Baker Street')

    if not Review.query.filter_by(user_id=lupin.id, place_id=place4.id).first():
        db.session.add(Review(
            text='I was invited. Then I was not. Then I was again. '
                 'The professor is a complicated host. The study is magnificent. '
                 'I would have taken the chess set, but it felt unsporting.',
            rating=3,
            user_id=lupin.id,
            place_id=place4.id
        ))
        print("Review created: Lupin -> The Spider's Web")

    if not Review.query.filter_by(user_id=ganimard.id, place_id=place6.id).first():
        db.session.add(Review(
            text='I arrived with a warrant. Lupin was gone. '
                 'The fireplace was still warm. The Calvados was excellent. '
                 'I stayed the night. I am not proud of this.',
            rating=3,
            user_id=ganimard.id,
            place_id=place6.id
        ))
        print('Review created: Ganimard -> Manoir de Gueures')

    if not Review.query.filter_by(user_id=ganimard.id, place_id=place5.id).first():
        db.session.add(Review(
            text='The pool is heated. The view is magnificent. '
                 'Lupin was gone before I reached the gate. '
                 'I am beginning to think he books these properties specifically '
                 'to make me travel.',
            rating=4,
            user_id=ganimard.id,
            place_id=place5.id
        ))
        print('Review created: Ganimard -> Villa Cagliostro')

    if not Review.query.filter_by(user_id=irene.id, place_id=place4.id).first():
        db.session.add(Review(
            text='The professor received me in the study. '
                 'The conversation was stimulating and mildly threatening. '
                 'The gas lighting suits the atmosphere perfectly. '
                 'I would not stay alone.',
            rating=3,
            user_id=irene.id,
            place_id=place4.id
        ))
        print("Review created: Irene -> The Spider's Web")

    if not Review.query.filter_by(user_id=watson.id, place_id=place8.id).first():
        db.session.add(Review(
            text='Holmes mentioned these rooms once, in passing. '
                 '"Before Baker Street," he said, and offered nothing further. '
                 'The desk by the window explains a great deal about the man.',
            rating=4,
            user_id=watson.id,
            place_id=place8.id
        ))
        print('Review created: Watson -> Montague Street Rooms')

    if not Review.query.filter_by(user_id=irene.id, place_id=place8.id).first():
        db.session.add(Review(
            text='A curious place. The library is exceptional for its size. '
                 'I found a notebook behind the third shelf — '
                 'I replaced it exactly where I found it. Mostly.',
            rating=4,
            user_id=irene.id,
            place_id=place8.id
        ))
        print('Review created: Irene -> Montague Street Rooms')

    if not Review.query.filter_by(user_id=watson.id, place_id=place9.id).first():
        db.session.add(Review(
            text='Holmes insisted I visit. The cottage is small, orderly in its own way, '
                 'and smells of beeswax and pipe tobacco. He made tea without being asked. '
                 'He seems, at last, content. I shall not say more.',
            rating=5,
            user_id=watson.id,
            place_id=place9.id
        ))
        print('Review created: Watson -> Sussex Downs Cottage')

    if not Review.query.filter_by(user_id=moriarty.id, place_id=place9.id).first():
        db.session.add(Review(
            text='I found it easily enough. The bees did not sting me. '
                 'Holmes was not surprised to see me. '
                 'We played chess for two hours and reached no conclusion. '
                 'The fireplace is adequate.',
            rating=3,
            user_id=moriarty.id,
            place_id=place9.id
        ))
        print('Review created: Moriarty -> Sussex Downs Cottage')

    db.session.commit()
    print('\nThe database has been successfully populated.')
