# Eventora

## Tech Stack:
### Frontend: React
### Backend: Python, Flask and MongoDB

## Entity Relationship Diagram

         +------------------------+       +--------------------+     +-------------------+
         |   EventOrganizer       |       |   VenueProvider    |     |      Audience     |
         +------------------------+       +--------------------+     +-------------------+
         | organizer_id int (PK)  |       | ProviderID (PK)    |     |  AudienceID (PK)  |
         | name varchar(255)      |       | Name               |     |  Name             |
         | email varchar(255)     |       | Address            |     |  Email            |
         | phone varchar(20)      |       | Contact Person     |     |  Phone            |
         | ...                    |       | ...                |     |  ...              |
         +------------------------+       +--------------------+     +-------------------+
                |                           |                         / | \
                | One Organizer              |                        /  |  \
                | can organize               |                One Audience Member can
                | Many Events                |               participate in Many Events
                |                           |                        /    \
                |                           |                       /      \
         +--------------+               +----------------+          /        \
         |    Event     |               |     Venue      |        /          \
         +--------------+               +----------------+       /            \
         | EventID (PK) |               | VenueID (PK)   |      /              \
         | Name         |               | Name           |     /                \
         | Description  |               | Address        |    /                  \
         | Date         |               | Capacity       |   /                    \
         | Time         |               | ...            |  /                      \
         | OrganizerID (FK) |          | ProviderID (FK) | /                        \
         +--------------+               +----------------+                          \
                                         | One Venue Provider can                 \
                                         | provide many Venues                    \
                                         |                                        \
                                         |                                        \
                                         |                                        \
                                  +----------------+                            \
                                  |   EventVenue   |                             \
                                  +----------------+                              \
                                  | EventVenueID   |                              \
                                  | EventID (FK)   |                               \
                                  | VenueID (FK)   |                                \
                                  | ...            |                                 \
                                  +----------------+                                  \
                                         |                                            \
                                         |                                            \
                                         |                                            \
                              +-----------------------+                              \
                              |       Ticket        |                               \
                              +-----------------------+                                \
                              | TicketID (PK)        |                                 \
                              | EventID (FK)         |                                  \
                              | AudienceID (FK)      |                                   \
                              | Price               |                                    \
                              | Quantity            |                                     \
                              | ...                 |                                      \
                              +-----------------------+


## API Endpoints

### User Management:

- POST /api/users - Create a new user.
- GET /api/users - Get a list of all users.
- GET /api/users/:id - Get a specific user by ID.
- PUT /api/users/:id - Update user information by ID.
- DELETE /api/users/:id - Delete a user by ID.

### Event Organizer:

- POST /api/event-organizers - Create a new event organizer.
- GET /api/event-organizers - Get a list of all event organizers.
- GET /api/event-organizers/:id - Get a specific event organizer by ID.
- PUT /api/event-organizers/:id - Update event organizer information by ID.
- DELETE /api/event-organizers/:id - Delete an event organizer by ID.

### Venue Provider:

- POST /api/venue-providers - Create a new venue provider.
- GET /api/venue-providers - Get a list of all venue providers.
- GET /api/venue-providers/:id - Get a specific venue provider by ID.
- PUT /api/venue-providers/:id - Update venue provider information by ID.
- DELETE /api/venue-providers/:id - Delete a venue provider by ID.

### Audience:

- POST /api/audiences - Create a new audience member.
- GET /api/audiences - Get a list of all audience members.
- GET /api/audiences/:id - Get a specific audience member by ID.
- PUT /api/audiences/:id - Update audience member information by ID.
- DELETE /api/audiences/:id - Delete an audience member by ID.

### Event Management:

- POST /api/events - Create a new event.
- GET /api/events - Get a list of all events.
- GET /api/events/:id - Get a specific event by ID.
- PUT /api/events/:id - Update event information by ID.
- DELETE /api/events/:id - Delete an event by ID.

### Venue Management:

- POST /api/venues - Create a new venue.
- GET /api/venues - Get a list of all venues.
- GET /api/venues/:id - Get a specific venue by ID.
- PUT /api/venues/:id - Update venue information by ID.
- DELETE /api/venues/:id - Delete a venue by ID.

### Ticket Booking:

- POST /api/tickets - Book a ticket for an event.
- GET /api/tickets - Get a list of all booked tickets.
- GET /api/tickets/:id - Get a specific ticket by ID.
- DELETE /api/tickets/:id - Cancel a booked ticket by ID.

### Movie Management:

- POST /api/movies - Add a new movie to the database.
- GET /api/movies - Get a list of all movies.
- GET /api/movies/:id - Get details of a specific movie by ID.
- PUT /api/movies/:id - Update movie details by ID.
- DELETE /api/movies/:id - Delete a movie by ID.

### Movie Show Management:

- POST /api/movie-shows - Add a new movie showtime.
- GET /api/movie-shows - Get a list of all movie showtimes.
- GET /api/movie-shows/:id - Get details of a specific movie showtime by ID.
- PUT /api/movie-shows/:id - Update movie showtime details by ID.
- DELETE /api/movie-shows/:id - Delete a movie showtime by ID.