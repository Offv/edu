-- Take a look to crime scene report for location
SELECT * FROM crime_scene_reports
WHERE month=7 and day>27 and street="Humphrey Street" and description LIKE "%duck%";
--Lets find interviews
SELECT DISTINCT * FROM interviews
WHERE year = 2023 and month=7 and day=28 and transcript LIKE "%thief%";

-- Get the name of the thief using all information from interviews
SELECT name FROM people
WHERE people.license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2023 and month=7 and day=28 and hour=10 and minute<25 and activity="exit")
-- Query ATM transactions
AND people.id IN (
-- Get person_id from the ATM transactions
SELECT person_id FROM bank_accounts
-- Let's join the bank account information so that we can grab the person_id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
-- Transaction was on the day of the crime
WHERE atm_transactions.year = 2023 AND atm_transactions.month = 7 AND atm_transactions.day = 28
-- It was a withdrawal
AND transaction_type = "withdraw" AND atm_location="Leggett Street")
-- Check Calls with our day
AND people.phone_number IN (SELECT caller FROM phone_calls WHERE year = 2023 and month=7 and day=28 and duration<60)
--Check who has flight next day
AND people.passport_number IN (SELECT passport_number FROM passengers WHERE flight_id IN (
SELECT id FROM flights WHERE year = 2023 AND month = 7 AND day = 29 and origin_airport_id= (
SELECT id FROM airports WHERE city ="Fiftyville") ORDER BY hour, minute ASC LIMIT 1));
--Name of suspect Bruce

-- Get the city name
SELECT city FROM airports
-- From the first flight of the day
WHERE id IN (
    SELECT destination_airport_id FROM flights WHERE year = 2023 AND month = 7 AND day = 29
    ORDER BY hour, minute ASC LIMIT 1
);
-- Destination New York City

-- Get the accomplice's name
SELECT name FROM people
-- Using their phone number
WHERE phone_number IN (
    -- From the list of phone calls
    SELECT receiver FROM phone_calls
    -- On the date of the crime
    WHERE year = 2023 AND month = 7 AND day = 28
    -- And where the caller was our criminal
    AND caller = (
    SELECT phone_number FROM people WHERE name =
    ("Bruce")) AND duration < 60);

--accomplice's name Robin


