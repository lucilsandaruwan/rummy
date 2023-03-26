import React, {useEffect, useState} from 'react';
import {Space, Table, Tag, Button} from 'antd';
import { fetchHands, acceptHand, declineHand } from '../actions/rummyActions';
import { connect, useDispatch } from 'react-redux';

const Home = ({pageData}) => {
    const dispatch = useDispatch();
    const {session} = pageData || {}
    const { hands } = session || {}
    useEffect(() => {
    //   dispatch(fetchHands());
    }, []);

    
    
    return (
        <div>
        <h2>Objective</h2>
Each player tries to lay all of the cards from their hands onto the table by forming matched sets. Valid sets must either be a 3-of-a-kind, 4-of-a-kind or a run with three or more cards.
<br/>
<h2>The Deal</h2>
The dealer gives one card at a time face down to each player,starting with the player to his left, in a clockwise direction. When two people play, each person gets 10 cards. When three or four people play, each person receives seven cards; when five or six people play, each receives six cards. The remaining cards are placed face down in the centre of the table, forming the stockpile.
The top card of the stock is turned and placed face-up next to the stockpile to form the discard pile. At the end of the round the position of dealer is passed to the left.
<br/>
<h2>The Play</h2>
Play begins with the person to the left of the dealer. There are four stages to each turn.
<h3>Draw (Compulsory)</h3> - Each player begins their turn by either drawing a single card from the top of the stockpile, or taking the top card from the discard pile. If you draw from stock, you add the card to your hand without showing it to the other players. If you draw a card from the discard pile you do the same but your opponents will know what card you have taken as the discard pile is face up and the top card can be seen by all players.
<h3>Melding (Optional)</h3> - Cards may be grouped and placed from your hand face-up on the table in front of you. Alternatively, you may choose to keep melds in your hand for reasons of strategy and/or the chance to gain a bonus. There are two kinds of combinations: Runs and Sets.
A Run (aka sequence) is three or more cards of the same suit in sequence and A Set (aka group) is three or four cards of the same rank and different suits.
<h3>Laying Off (Optional)</h3>  - This involves adding cards from your hand to melds previously placed on the table by yourself or other players. Cards added must form a legitimate meld. Thus, if there is a run of 4♠ 5♠ 6♠ on the table, you may add 3♠ or you could add 2♠ and 3♠ or even 2♠ 3♠ and 7♠. You are not permitted to move cards from one meld to another to form new melds. You are not obligated to lay off cards just because you can but there is no limit to the number of cards you can lay off during a single turn. A popular variation of the game forbids players from
laying off until they have laid at least one of their own melds on the table first.
Discarding (Compulsory) - This is where you place a card from your hand on the discard pile. Each player must end their turn by discarding one card from his hand face up on the discard pile. Once the player has discarded, his turn is over and he may not play any cards again until the turn moves back to him.
If the stock pile runs out, the top card from the discard pile is set aside and the remainder of the discard pile is shuffled and turned face down to become the new stockpile. The top card starts the new discard pile.
A player wins the hand by being the first to play all the cards in their hand by either melding, laying off or discarding. Once a player has gone out, the hand is ended. No other players may meld, lay off or discard their cards even if they have valid combinations already in their hand.
A player "goes out" when he gets rid of all his cards and he therefore wins the game. If all his remaining cards are melded, he may lay them down without discarding a card to end his last turn. This ends the game and there is no further play.
A player "goes Rummy" when he disposes of all the cards in his hand in one turn and goes out without previously having put down melds in the meld area or laid off any cards against existing melds that have already been placed there. When this happens, every other player earns him twice the amount of points they would ordinarily owe.
Scoring
At the end of the hand, each player adds up the points of the cards remaining in his or her hand as follows:
● Faces (King, Queen and Jack) are worth 10 points each.
The total value of all cards remaining in the hands of other players is added to the cumulative score of the winning player. The game can continue with further hands until a previously agreed upon target score is reached (100 points by default). Another popular variation exists where instead of the winner scoring points, each of the losers score penalty points according to the cards left in their hand.
Variations
1. You may only lay down one meld during a turn.
●
worth eight points, etc.
is worth 5 points, an8   is
Number cards are worth their pip value, for example: 5 ● Aces are low in this game and worth 1 point each.

2. A player cannot lay off any cards unless they have put down at least one meld of their own.
3. If you draw from the discard pile you cannot discard the same card in the same turn.
4. The game ends when the stock pile runs out with players then scoring the value of the cards left in their hand.
5. A player who has not previously melded or laid off any cards earns a bonus if they can go out in a single turn by melding or laying off their entire hand and some house rules may provide that this is 10 points and not a doubling of points owed.
6. Aces can be counted as high or low, so that Q-K-A and sometimes also K-A-2 (round the corner) are valid runs. They are not valid in the default game as Aces are low. When Aces are counted as both high and low, they are usually given the value of 15 points (instead of 1 point) to offset the enhanced usage possibilities.
7. In order to go out, you must end your turn by discarding your last card.
8. Values in the hand at the end of the round are added to the player’s own score as a penalty. In that case, the player with the lowest score at the end of the specified number of rounds or when the target score is reached, is the winner.
    </div>
    )
};

// export default LoginForm;
const mapStateToProps = state => ({
    pageData: {...state}
  });
  
  export default connect(mapStateToProps, {fetchHands, acceptHand, declineHand})(Home);