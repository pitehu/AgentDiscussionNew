# discussion_modes.py

import random
from config import get_max_responses
import logging

class GenericDiscussionMode:
    def __init__(self, conversation, task_config, message_strategy):
        self.conversation = conversation
        self.task_config = task_config
        self.message_strategy = message_strategy
        self.data_strategy = conversation.data_strategy
        self.max_responses = get_max_responses(task_config.get("phases","three_stage"))
        logging.info("Discussion mode initialized with task configuration: %s", self.task_config)

    # def run(self):
    #     phases= self.task_config.get("phases","three_stage")
    #     if phases=="three_stage":
    #         self.run_generation()
    #         self.run_selection()
    #         self.run_discussion()
    #     else:
    #         self.run_direct_discussion()
        
    #     print("\n=== Final Token Usage Summary ===")
    #     print(self.conversation.get_token_summary())

    def run(self, skip_to_discussion=False):
        phases= self.task_config.get("phases","three_stage")
        if phases == "three_stage":
            if not skip_to_discussion:
                phases = self.task_config.get("phases", "three_stage")   
                self.run_generation()
                self.run_selection()
            else:
                # Example preloaded ideas and rankings
                # 初始化所有想法
                # self.data_strategy.all_ideas = [
                #     {"idea": "Create a portable clothesline for camping by suspending rope between trees.", "agent": "CFO"},
                #     {"idea": "Fashion a quick improvised belt for holding up trousers in an emergency.", "agent": "CFO"},
                #     {"idea": "Use rope as a makeshift hammock for relaxation in a pinch.", "agent": "CFO"},
                #     {"idea": "Construct a DIY jump rope for a fun workout alternative.", "agent": "CFO"},
                #     {"idea": "Generate a unique wall decoration by weaving colorful rope into shapes.", "agent": "CFO"},
                #     {"idea": "DIY vertical garden trellis for trailing plants indoors or outdoors.", "agent": "CTO"},
                #     {"idea": "Emergency leash for pets in unexpected situations.", "agent": "CTO"},
                #     {"idea": "Portable clothesline for drying clothes on camping trips.", "agent": "CTO"},
                #     {"idea": "Backpack hydration system to secure water bottles for hiking.", "agent": "CTO"},
                #     {"idea": "Art installation tool for creating 3D sculptures in galleries.", "agent": "CTO"},
                #     {"idea": "Emergency fishing line for catching small fish in survival situations.", "agent": "CEO"},
                #     {"idea": "Makeshift belt for securing loose clothing or gear.", "agent": "CEO"},
                #     {"idea": "Temporary dog leash in a pinch for pet safety.", "agent": "CEO"},
                #     {"idea": "Decorative wall art by weaving colorful rope patterns.", "agent": "CEO"},
                #     {"idea": "Garden trellis support for climbing plants and vegetables.", "agent": "CEO"}
                # ]

                # # 初始化每个 agent 的选择
                # self.data_strategy.agent_selected_ideas = {
                #     "CEO": [0, 10, 2, 5, 3],
                #     "CTO": [1, 2, 5, 10, 9],
                #     "CFO": [0, 1, 6, 10, 5]
                # }

                self.data_strategy.ranked_ideas = [
                    "Implement a 'Wellness Swap' program where employees can exchange skills or activities (like yoga sessions, cooking classes, etc.) to foster community, promote mental health, and encourage holistic wellbeing.",
                    "Create a 'Nature Day,' allowing employees to work remotely from a nature location, encouraging outdoor time, reducing stress, and enhancing creativity.",
                    "Introduce a digital 'Wellbeing Buddy' app that pairs employees with a peer for regular check-ins, support, and friendly challenges, fostering connection and accountability in maintaining wellbeing.",
                    "Implement a 'Wellness Buddy' program, pairing employees for regular check-ins and support through fitness activities, mental health discussions, and shared wellness challenges.",
                    "Create a virtual 'Personal Growth Fund' allowing employees to access a budget for activities like courses, therapy, or wellness retreats focused on their wellbeing.",
                    "Launch a 'Mood Docket' app where employees anonymously share daily sentiments, fostering open dialogue and building a collective understanding of workplace wellbeing needs.",
                    "Implement a 'Wellbeing Exchange' platform where employees can trade unused wellness days for points redeemable for mental health services or fitness classes.",
                    "Create a virtual reality relaxation room where employees can escape to calming environments and participate in guided meditation sessions during breaks.",
                    "Introduce 'Wellness Ambassadors,' trained employees who promote healthy habits, support peers, and organize regular activities focusing on physical and mental health.",
                    "Develop a 'Wellbeing Mentor' initiative where experienced staff members guide others in maintaining mental and physical health routines.",
                    "Organize a quarterly 'Wellness Day' where the company hosts events like mindfulness workshops, fitness challenges, or healthy cooking classes.",
                    "Create a 'Mindfulness Library' of curated resources, including books, podcasts, and videos, for employees to access on demand.",
                    "Launch a 'Wellbeing Dashboard' that provides employees with personalized recommendations for improving their physical and mental health based on self-reported data.",
                    "Host an annual 'Health Fair' offering free health screenings, wellness seminars, and opportunities to explore mental and physical health resources.",
                    "Develop an 'Active Breaks' program encouraging employees to participate in brief, guided physical activities during work hours to reduce stress and boost energy levels."
                ]

                print("Predefined ranked ideas loaded.")
            self.run_discussion()
        else:
            self.run_direct_discussion()
        print("\n=== Final Token Usage Summary ===")
        print(self.conversation.get_token_summary())



    # ---------------- Generation ----------------
    def run_generation(self):
        print("Starting idea generation phase.")
        agents= self.conversation.agents[:]
        if self.task_config.get("discussion_order_method")=="random":
            random.shuffle(agents)

        for ag in agents:
            self.conversation.current_agent= ag
            msgs= self.message_strategy.construct_messages(ag, 'idea_generation', self.conversation)

            # Generate response and get token usage
            resp, prompt_tokens, completion_tokens = ag.generate_response(msgs)
            self.conversation.add_chat_entry(ag.name, "\n".join(m['content'] for m in msgs), resp, 'idea_generation')

            # Update token usage
            self.conversation.update_phase_token_usage("idea_generation", prompt_tokens, completion_tokens)

            self.data_strategy.collect_ideas(ag.name, resp)
            
            logging.debug("Agent %s generated ideas: %s", ag.name, resp)

        # Print token usage summary for the generation phase
        print("\n=== Token Usage Summary (Generation Phase) ===")
        print(self.conversation.get_token_summary())

    # ---------------- Selection ----------------
    def run_selection(self):
        print("Starting selection phase.")
        agents= self.conversation.agents[:]
        sel_method= self.task_config.get("selection_method","rating")
        if self.task_config.get("discussion_order_method")=="random":
            random.shuffle(agents)

        for ag in agents:
            self.conversation.current_agent= ag
            msgs= self.message_strategy.construct_messages(ag, 'selection', self.conversation)

            lines=[f"Idea {i+1}: {x['idea']}" for i,x in enumerate(self.data_strategy.all_ideas)]
            msgs.append({"role":"assistant","content":"\n".join(lines)})

            # Generate response and get token usage
            resp, prompt_tokens, completion_tokens = ag.generate_response(msgs)
            self.conversation.add_chat_entry(ag.name, "\n".join(m['content'] for m in msgs), resp, 'selection')

            # Update token usage
            self.conversation.update_phase_token_usage("selection",prompt_tokens, completion_tokens)

            if sel_method=="rating":
                self.data_strategy.collect_scores(ag.name, resp)
            else:
                self.data_strategy.collect_selections(ag.name, resp)

        if sel_method=="rating":
            self.data_strategy.calculate_rankings_by_average(self.conversation)
        
        # Print token usage summary for the generation phase
        print("\n=== Token Usage Summary (Selection Phase) ===")
        print(self.conversation.get_token_summary())


    # ---------------- Discussion ----------------
    def run_discussion(self):
        print("Starting discussion phase.")
        self.data_strategy.first_agent_name= None  # optional clear
        disc_method= self.task_config.get("discussion_method","all_at_once")
        if disc_method=="all_at_once":
            self.discussion_all_at_once()
        else:
            self.discussion_one_by_one()
        
        # Print token usage summary for the discussion phase
        print("\n=== Token Usage Summary (Discussion Phase) ===")
        print(self.conversation.get_token_summary())

    def discussion_all_at_once(self):
        """
        Handle (rating) or (selectionTop), for AUT or PS.
        If rating => init topN + replacement + left
        If selectionTop => first time pick agent => use their picks => ...
        Then each agent can replace/modify/no-objection
        """
        self.data_strategy.reset_agreements()
        sel_method= self.task_config.get("selection_method","rating")
        ttype= self.task_config.get("task_type","AUT")

        # rating => init
        if sel_method=="rating":
            if ttype=="AUT":
                # top5, next5
                self.data_strategy.current_ideas= self.data_strategy.ranked_ideas[:5]
                self.data_strategy.replacement_ideas= self.data_strategy.ranked_ideas[5:10]
                self.data_strategy.left= self.data_strategy.ranked_ideas[10:]
            else:
                # PS => top1, next3
                self.data_strategy.current_ideas= self.data_strategy.ranked_ideas[:1]
                self.data_strategy.replacement_ideas= self.data_strategy.ranked_ideas[1:4]
                self.data_strategy.left= self.data_strategy.ranked_ideas[4:]
        # selectionTop => do not init yet, will do in the loop if first_agent not set

        total_resp=0
        while total_resp< self.max_responses:
            remain= [ag for ag in self.conversation.agents if not self.data_strategy.agent_has_agreed(ag.name)]
            if not remain:
                print("All agents agreed(all_at_once).")
                self._print_final()
                return
            agent = self._select_next_agent(remain)

            # if not first_agent_name => set it => if selectionTop => init from that agent picks
            if sel_method=="selectionTop": 
                if not self.data_strategy.first_agent_name:
                    self.data_strategy.first_agent_name= agent.name
                    # AUT => that agent's top5 => current_ideas
                    if ttype=="AUT":
                        idxs= self.data_strategy.agent_selected_ideas.get(agent.name, [])
                        all_txt= self.data_strategy.all_ideas
                        # convert idx -> text
                        cIdeas=[]
                        for i in idxs:
                            if 0<= i< len(all_txt):
                                cIdeas.append(all_txt[i]['idea'])
                        cIdeas= cIdeas[:5]
                        self.data_strategy.current_ideas= cIdeas
                        self.data_strategy.agent_replacement_ideas[agent.name] = []  # or empty
                    else:
                        # PS => top3 => [0]= current, [1,2] => replacement
                        idxs= self.data_strategy.agent_selected_ideas.get(agent.name, [])
                        sol_txt= [x['idea'] for x in self.data_strategy.all_ideas]
                        c=[]
                        rep=[]
                        if idxs:
                            if 0<= idxs[0]< len(sol_txt):
                                c.append(sol_txt[idxs[0]])
                            for x in idxs[1:]:
                                if 0<=x< len(sol_txt):
                                    rep.append(sol_txt[x])
                        self.data_strategy.current_ideas= c[:1]
                        self.data_strategy.agent_replacement_ideas[agent.name]= rep[:2]
                else:
                    if agent.name not in self.data_strategy.agent_replacement_ideas:
                        if ttype == "AUT":
                            idxs = self.data_strategy.agent_selected_ideas.get(agent.name, [])
                            all_txt = self.data_strategy.all_ideas
                            self.data_strategy.agent_replacement_ideas[agent.name] = [
                                all_txt[i]['idea'] for i in idxs if 0 <= i < len(all_txt)
                            ][:5]
                        else:  # PS case
                            idxs = self.data_strategy.agent_selected_ideas.get(agent.name, [])
                            sol_txt = [x['idea'] for x in self.data_strategy.all_ideas]
                            self.data_strategy.agent_replacement_ideas[agent.name] = [
                                sol_txt[i] for i in idxs if 0 <= i < len(sol_txt)
                            ][:3]
            self.conversation.current_agent= agent
            msgs= self.message_strategy.construct_messages(agent,'discussion',self.conversation,total_resp=total_resp)
            resp, prompt_tokens, completion_tokens = agent.generate_response(msgs)
            self.conversation.add_chat_entry(agent.name, "\n".join(m['content'] for m in msgs), resp, 'discussion')

            # Update token usage
            self.conversation.update_phase_token_usage("discussion",prompt_tokens, completion_tokens)

            print(f"[all_at_once] {agent.name} => {resp}")

            self.data_strategy.update_shared_data(self.conversation, resp)
            total_resp+=1

            if self.data_strategy.all_agents_agreed(self.conversation.agents):
                print("All agents agreed(all_at_once).")
                self._print_final()
                return

        print("max responses(all_at_once) => no full agreement.")
        self._print_final()

    def discussion_one_by_one(self):
        """
        4 scenarios:
          - rating => keep leftover => next idea from leftover[0]
          - selectionTop => each round pick new first_agent => ...
        Only AUT (PS is skipped).
        """
        if self.task_config.get("task_type","AUT")!="AUT":
            print("PS + one_by_one not supported.")
            return

        sel_method= self.task_config.get("selection_method","rating")

        if sel_method=="rating":
            # Suppose we have 15 ideas in ranked_ideas.
            # We'll do 5 rounds => each round:
            # Round1 => current_ideas= [ranked_ideas[0]], replacement_ideas= [ranked_ideas[1..5]], leftover= [6..]
            # After the round, if no new replacement usage or partial usage => next round
            # set current_ideas= [ replacement_ideas[0] ] or leftover[0], depends on your logic
            # Here we do a demonstration
            self.discussion_one_by_one_rating_mode()
        else:
            self.discussion_one_by_one_selectionTop_mode()

    def discussion_one_by_one_rating_mode(self):
        """
        Example logic: 
        Round1 => current_ideas= [ranked_ideas[0]], replacement= [1..5], left= [6..]
        Round2 => new idea from leftover or from replacement leftover
        ...
        """
        ideas_list= self.data_strategy.ranked_ideas
        total_ideas= len(ideas_list)
        if total_ideas<1:
            print("No ideas for one_by_one rating.")
            return

        # Start with first idea
        # e.g. Round1
        current_idx=0
        self.data_strategy.current_idea_index= 0

        # init
        self.data_strategy.current_ideas= [ideas_list[0]]
        self.data_strategy.replacement_ideas= ideas_list[1:6]
        self.data_strategy.left= ideas_list[6:]

        round_count= 5  # we want 5 ideas total
        final_ideas = []  # track used

        for round_i in range(round_count):
            self.data_strategy.reset_agreements()
            if round_i==0:
                # use the already init
                pass
            else:
                # new round => current idea from leftover approach:
                # Step 1: Use the first idea from replacement_ideas as the current idea
                if self.data_strategy.replacement_ideas:
                    new_idea = self.data_strategy.replacement_ideas.pop(0)
                    self.data_strategy.current_ideas = [new_idea]

                # Step 2: Refill replacement_ideas from left to maintain the desired size
                desired_size = 5  # Adjust based on task requirements
                while len(self.data_strategy.replacement_ideas) < desired_size:
                    if self.data_strategy.left:
                        self.data_strategy.replacement_ideas.append(self.data_strategy.left.pop(0))
                    else:
                        print("No more leftover ideas!")
                        break

            local_res=0

            while local_res<10:
                remain= [ag for ag in self.conversation.agents if not self.data_strategy.agent_has_agreed(ag.name)]
                if not remain:
                    print(f"Round {round_i+1} => all agreed.")
                    break

                agent = self._select_next_agent(remain)

                self.conversation.current_agent= agent
                msgs= self.message_strategy.construct_messages(agent,'discussion', self.conversation, idea_index=round_i,current_round=local_res + 1, max_rounds=10)
                resp, prompt_tokens, completion_tokens = agent.generate_response(msgs)
                self.conversation.add_chat_entry(agent.name, "\n".join(m['content'] for m in msgs), resp, 'discussion', round_i)

                # Update token usage
                self.conversation.update_phase_token_usage("discussion",prompt_tokens, completion_tokens)

                print(f"[one_by_one+rating Round {round_i+1}] {agent.name} => {resp}")
                self.data_strategy.update_shared_data(self.conversation, resp)
                local_res+=1

            print(f"End Round {round_i+1} => final idea: {self.data_strategy.current_ideas[0]}")
            final_ideas.append(self.data_strategy.current_ideas[0])

        print("One_by_one + rating done.")
        print("\n=== Final AUT ideas ===")
        for i, idea in enumerate(final_ideas, 1):
            print(f"{i}. {idea}")


    def discussion_one_by_one_selectionTop_mode(self):
        """
        Each round => we handle 1 idea from an agent's top picks.
        A. first round => no first_agent => the first who speaks becomes first_agent => use agent's picks => set current_ideas= [picks[0]]? 
        B. other agents => they have their own picks in agent_replacement_ideas => can do replace. 
        C. end of round => clear first_agent => next round => new first_agent or the same.
        """

        round_count= 5  # want 5 final ideas
        ttype= self.task_config.get("task_type","AUT")

        # Step 1: Initialize replacement_ideas for all agents
        all_txt = [x['idea'] for x in self.data_strategy.all_ideas]
        for ag in self.conversation.agents:
            if ag.name not in self.data_strategy.agent_replacement_ideas:
                idxs = self.data_strategy.agent_selected_ideas.get(ag.name, [])
                rep_list = [all_txt[i] for i in idxs if 0 <= i < len(all_txt)]
                self.data_strategy.agent_replacement_ideas[ag.name] = rep_list

        # List to store the final ideas for each round
        final_ideas = []

        for r in range(round_count):
            self.data_strategy.reset_agreements()
            self.data_strategy.current_idea_index= r
            self.data_strategy.current_ideas= []
            # For clarity, we do not unify leftover logic here. We rely on each agent's picks. 

            local_res=0
            while local_res<10:
                remain= [ag for ag in self.conversation.agents if not self.data_strategy.agent_has_agreed(ag.name)]
                if not remain:
                    print(f"[one_by_one+selectionTop] Round {r+1} => all agreed.")
                    break

                chosen = self._select_next_agent(remain)

                # if there's no first_agent => set chosen as first_agent => init current_ideas from chosen picks (the r'th pick).
                if not self.data_strategy.first_agent_name:
                    self.data_strategy.first_agent_name = chosen.name
                    first_agent_repl = self.data_strategy.agent_replacement_ideas.get(chosen.name, [])
                    if first_agent_repl:
                        current_idea = first_agent_repl.pop(0)  # Take the first idea
                        self.data_strategy.current_ideas = [current_idea]
                        self.data_strategy.agent_replacement_ideas[chosen.name] = first_agent_repl
                    else:
                        self.data_strategy.current_ideas = ["(no valid ideas)"]
                        print(f"{chosen.name} has no replacement ideas remaining.")

                # Let chosen agent speak
                self.conversation.current_agent= chosen
                msgs= self.message_strategy.construct_messages(chosen,'discussion', self.conversation, r,current_round=local_res + 1, max_rounds=10)
                resp, prompt_tokens, completion_tokens = chosen.generate_response(msgs)
                self.conversation.add_chat_entry(chosen.name, "\n".join(m['content'] for m in msgs), resp, 'discussion', r)

                # Update token usage
                self.conversation.update_phase_token_usage("discussion",prompt_tokens, completion_tokens)
                print(f"[one_by_one+selectionTop Round {r+1}] {chosen.name} => {resp}")
                self.data_strategy.update_shared_data(self.conversation, resp)
                local_res+=1
            
            # Store the final idea for this round
            final_ideas.append(self.data_strategy.current_ideas[0])
            print(f"[one_by_one+selectionTop] Round {r+1} ended => final idea: {self.data_strategy.current_ideas[0]}")
            self.data_strategy.first_agent_name= None  # so next round can pick new first_agent if needed

        print("one_by_one + selectionTop completed.")
        # Print and store the final list of 5 ideas
        self.data_strategy.current_ideas = final_ideas

        print("\n=== Final AUT ideas ===")
        for i, idea in enumerate(final_ideas, 1):
            print(f"{i}. {idea}")


    def run_direct_discussion(self):
        """
        Handles the direct discussion phase.
        Supports AUT and PS tasks with either "all_at_once" or "one_by_one" methods.
        """
        print("Starting direct discussion phase.")
        self.data_strategy.first_agent_name = None  # Reset first agent tracking.

        task_type = self.task_config.get("task_type", "AUT")
        discussion_method = self.task_config.get("discussion_method", "all_at_once")

        if task_type == "AUT":
            if discussion_method == "all_at_once":
                self.direct_discussion_aut_all_at_once()
            elif discussion_method == "one_by_one":
                self.direct_discussion_aut_one_by_one()
        elif task_type == "PS":
            self.direct_discussion_ps_all_at_once()

        print("\n=== Final Token Usage Summary ===")
        print(self.conversation.get_token_summary())

    def direct_discussion_aut_all_at_once(self):
        """
        Direct discussion for AUT with all_at_once.
        """
        print("[direct_discussion_aut_all_at_once] Starting...")
        self.data_strategy.current_ideas = []  # Clear current ideas initially.
        total_resp = 0

        while total_resp < self.max_responses:      
            remain = [ag for ag in self.conversation.agents if not self.data_strategy.agent_has_agreed(ag.name)]
            if not remain:
                print("All agents agreed (AUT all_at_once direct discussion).")
                break
            agent = self._select_next_agent(remain)
            self.conversation.current_agent = agent

            msgs = self.message_strategy.construct_messages(agent, 'direct', self.conversation, total_resp=total_resp)
            resp, prompt_tokens, completion_tokens = agent.generate_response(msgs)
            if total_resp == 0:
                self.data_strategy.current_ideas = [resp]
            self.conversation.add_chat_entry(agent.name, "\n".join(m["content"] for m in msgs), resp, "direct")

            # Update token usage
            self.conversation.update_phase_token_usage("discussion",prompt_tokens, completion_tokens)

            print(f"[AUT all_at_once direct] {agent.name} => {resp}")

            # Update shared data
            if total_resp != 0:
                self.data_strategy.update_shared_data(self.conversation, resp)
            total_resp += 1

        print("[direct_discussion_aut_all_at_once] Completed.")

    def direct_discussion_aut_one_by_one(self):
        """
        Direct discussion for AUT with one_by_one.
        Each idea has up to 15 rounds of discussion.
        """
        print("[direct_discussion_aut_one_by_one] Starting...")
        self.data_strategy.current_ideas = []  # Clear current ideas initially.
        round_count = 5  # Number of ideas to finalize.
        max_rounds_per_idea = 15  # Maximum rounds for each idea.
        final_ideas = []  # Store finalized ideas.

        for idea_idx in range(round_count):
            self.data_strategy.reset_agreements()
            self.data_strategy.current_ideas = []  # Reset current ideas for the new idea.

            total_resp_per_idea = 0  # Reset response count for the current idea.

            while total_resp_per_idea < max_rounds_per_idea:
                remain = [
                    ag for ag in self.conversation.agents
                    if not self.data_strategy.agent_has_agreed(ag.name)
                ]
                if not remain:
                    print(f"All agents agreed for idea #{idea_idx + 1}. Moving to the next idea.")
                    break

                # Determine the next agent to respond.
                agent = self._select_next_agent(remain)
                self.conversation.current_agent = agent

                msgs = self.message_strategy.construct_messages(
                    agent, "direct", self.conversation, current_round=total_resp_per_idea + 1, idea_index = idea_idx
                )
                resp, prompt_tokens, completion_tokens = agent.generate_response(msgs)
                if total_resp_per_idea == 0:
                    self.data_strategy.current_ideas = [resp]
                self.conversation.add_chat_entry(
                    agent.name, "\n".join(m["content"] for m in msgs), resp, "direct", idea_index=idea_idx
                )

                # Update token usage.
                self.conversation.update_phase_token_usage("discussion",prompt_tokens, completion_tokens)

                print(f"[One_by_one] Agent {agent.name} responded: {resp}")

                # Update shared data.
                if total_resp_per_idea != 0:
                    self.data_strategy.update_shared_data(self.conversation, resp)

                total_resp_per_idea += 1

            print(f"Discussion for idea #{idea_idx + 1} completed. Final idea: {self.data_strategy.current_ideas[0]}")
            final_ideas.append(self.data_strategy.current_ideas[0])

        print("\n=== Final Ideas ===")
        for i, idea in enumerate(final_ideas, 1):
            print(f"{i}. {idea}")

        print("[direct_discussion_aut_one_by_one] Completed.")


    # PS direct discussion only supports all_at_once
    def direct_discussion_ps_all_at_once(self):
        """
        Direct discussion for PS with all_at_once.
        """
        print("[direct_discussion_ps_all_at_once] Starting...")
        self.data_strategy.current_ideas = []  # Clear current ideas initially.
        total_resp = 0
        while total_resp < self.max_responses:
            remain = [ag for ag in self.conversation.agents if not self.data_strategy.agent_has_agreed(ag.name)]
            if not remain:
                print("All agents agreed (AUT all_at_once direct discussion).")
                break
            agent = self._select_next_agent(remain)
            self.conversation.current_agent = agent
            msgs = self.message_strategy.construct_messages(agent, "direct", self.conversation, total_resp=total_resp)
            resp, prompt_tokens, completion_tokens = agent.generate_response(msgs)
            if total_resp == 0:
                self.data_strategy.current_ideas = [resp]
            self.conversation.add_chat_entry(agent.name, "\n".join(m["content"] for m in msgs), resp, "direct")
            if total_resp != 0:
                self.data_strategy.update_shared_data(self.conversation, resp)
            self.conversation.update_phase_token_usage("discussion",prompt_tokens, completion_tokens)
            
            print(f"[PS all_at_once direct] {agent.name} => {resp}")
            total_resp += 1
        print("[direct_discussion_ps_all_at_once] Completed.")


    def _print_final(self):
        ttype= self.task_config.get("task_type","AUT")
        if ttype=="AUT":
            print("\n=== Final AUT ideas ===")
            for i, idea in enumerate(self.data_strategy.current_ideas, 1):
                print(f"{i}. {idea}")
        else:
            print("\n=== Final PS ideas ===")
            for i, sol in enumerate(self.data_strategy.current_ideas, 1):
                print(f"{i}. {sol}")

    def _select_agent_by_intention(self, candidates):
        """
        Collects intention scores from candidates and selects the agent with the highest score.
        """
        print("\n=== Select agents ===")
        for agent in candidates:
            self.conversation.current_agent = agent
            msgs = self.message_strategy.construct_messages(agent, "discussion", self.conversation, include_intention_prompt=True)
            resp, prompt_tokens, completion_tokens = agent.generate_response(msgs)
            try:
                self.data_strategy.collect_intention_score(agent.name, resp)
                self.conversation.add_chat_entry(agent.name, "\n".join(m["content"] for m in msgs), resp, "intention_score")
                self.conversation.update_phase_token_usage("discussion",prompt_tokens, completion_tokens)
            except ValueError:
                print(f"Invalid score '{resp}' from {agent.name}. Defaulting to 0.")
                self.data_strategy.collect_intention_score(agent.name, 0)

        # Get the agent with the highest score
        selected_agent = self.data_strategy.get_highest_intention_agent(candidates)
        print(f"Selected {selected_agent.name} with the highest intention score.")
        return selected_agent

    def _select_next_agent(self, remain):
        """
        Selects the next agent based on the discussion order method.
        """
        disc_order = self.task_config.get("discussion_order_method", "fixed")
        if disc_order == "hand_raising":
            return self._select_agent_by_intention(remain)
        elif disc_order == "random":
            return random.choice(remain)
        else:
            return remain[0]