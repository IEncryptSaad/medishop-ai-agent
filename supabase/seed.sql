-- Demo seed data for local Supabase development.
-- Uses fixed UUIDs so conversations, tickets, and appointments remain easy to inspect.

insert into public.users (id, email, full_name, phone, role, metadata_json) values
  ('10000000-0000-0000-0000-000000000001', 'maya.patient@example.com', 'Maya Patient', '+1-555-0101', 'customer', '{"preferred_channel":"web"}'),
  ('10000000-0000-0000-0000-000000000002', 'sam.caregiver@example.com', 'Sam Caregiver', '+1-555-0102', 'customer', '{"preferred_channel":"email"}'),
  ('10000000-0000-0000-0000-000000000003', 'alex.staff@medishop.example', 'Alex Support', '+1-555-0199', 'staff', '{}')
on conflict (id) do nothing;

insert into public.product_categories (id, name, slug, description) values
  ('20000000-0000-0000-0000-000000000001', 'Mobility Aids', 'mobility-aids', 'Canes, walkers, and accessories for safer movement.'),
  ('20000000-0000-0000-0000-000000000002', 'Home Diagnostics', 'home-diagnostics', 'At-home monitoring devices and test supplies.'),
  ('20000000-0000-0000-0000-000000000003', 'Respiratory Care', 'respiratory-care', 'Respiratory therapy supplies and maintenance items.'),
  ('20000000-0000-0000-0000-000000000004', 'Daily Living', 'daily-living', 'Assistive products for comfort and independence.')
on conflict (id) do nothing;

insert into public.products (id, category_id, sku, name, description, price, stock_quantity, status, attributes) values
  ('30000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001', 'MS-CANE-ADJ-BLK', 'Adjustable Aluminum Cane', 'Lightweight cane with ergonomic handle and anti-slip rubber tip.', 24.99, 48, 'active', '{"brand":"MediStep","color":"black","height_range":"30-39 inches"}'),
  ('30000000-0000-0000-0000-000000000002', '20000000-0000-0000-0000-000000000002', 'MS-BP-MON-ARM', 'Automatic Upper Arm Blood Pressure Monitor', 'Clinically validated monitor with large display and two-user memory.', 59.95, 26, 'active', '{"brand":"CardioHome","cuff_size":"standard/large","fsa_hsa_eligible":true}'),
  ('30000000-0000-0000-0000-000000000003', '20000000-0000-0000-0000-000000000002', 'MS-PULSE-OX-FING', 'Fingertip Pulse Oximeter', 'Portable oxygen saturation and pulse rate monitor with carrying case.', 34.50, 35, 'active', '{"brand":"OxiQuick","batteries_included":true}'),
  ('30000000-0000-0000-0000-000000000004', '20000000-0000-0000-0000-000000000003', 'MS-NEB-KIT-ADULT', 'Adult Nebulizer Replacement Kit', 'Replacement tubing, medicine cup, and adult mask for compatible nebulizers.', 18.75, 60, 'active', '{"brand":"BreatheWell","latex_free":true}'),
  ('30000000-0000-0000-0000-000000000005', '20000000-0000-0000-0000-000000000004', 'MS-PILL-ORG-WEEK', 'Weekly Pill Organizer', 'Seven-day pill organizer with morning and evening compartments.', 9.99, 120, 'active', '{"brand":"MediSort","compartments":14}')
on conflict (id) do nothing;

insert into public.knowledge_documents (id, title, source_type, source_uri, status, metadata_json) values
  ('40000000-0000-0000-0000-000000000001', 'Shipping and Delivery FAQ', 'faq', 'internal://faq/shipping', 'indexed', '{"audience":"customers"}'),
  ('40000000-0000-0000-0000-000000000002', 'Returns and Hygiene Policy', 'policy', 'internal://policy/returns', 'indexed', '{"audience":"customers"}'),
  ('40000000-0000-0000-0000-000000000003', 'Blood Pressure Monitor Setup Guide', 'product_guide', 'internal://guides/bp-monitor', 'indexed', '{"product_sku":"MS-BP-MON-ARM"}'),
  ('40000000-0000-0000-0000-000000000004', 'Appointment Types FAQ', 'faq', 'internal://faq/appointments', 'indexed', '{"audience":"customers"}')
on conflict (id) do nothing;

insert into public.knowledge_chunks (document_id, chunk_index, content, token_count, metadata_json) values
  ('40000000-0000-0000-0000-000000000001', 0, 'Standard shipping usually arrives in 3 to 5 business days. Expedited shipping options may be available at checkout for eligible items.', 24, '{"topic":"shipping"}'),
  ('40000000-0000-0000-0000-000000000001', 1, 'Orders containing regulated or oversized medical equipment may require additional verification before shipment.', 16, '{"topic":"shipping_verification"}'),
  ('40000000-0000-0000-0000-000000000002', 0, 'Unopened products may be returned within 30 days. Opened hygiene products, masks, and personal care items are generally not returnable unless defective.', 26, '{"topic":"returns"}'),
  ('40000000-0000-0000-0000-000000000003', 0, 'To use the upper arm blood pressure monitor, sit upright, rest for five minutes, place the cuff above the elbow, and keep the cuff at heart level.', 31, '{"topic":"setup","sku":"MS-BP-MON-ARM"}'),
  ('40000000-0000-0000-0000-000000000004', 0, 'Customers can request pharmacist consultations, product setup calls, and order support appointments. Appointment requests are confirmed by staff before they are final.', 24, '{"topic":"appointments"}')
on conflict (document_id, chunk_index) do nothing;

insert into public.appointments (id, user_id, appointment_type, scheduled_start, scheduled_end, status, notes, metadata_json) values
  ('50000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000001', 'product_setup', now() + interval '2 days', now() + interval '2 days 30 minutes', 'scheduled', 'Help setting up the blood pressure monitor.', '{"product_sku":"MS-BP-MON-ARM"}'),
  ('50000000-0000-0000-0000-000000000002', '10000000-0000-0000-0000-000000000002', 'pharmacist_consult', now() + interval '4 days', now() + interval '4 days 45 minutes', 'requested', 'Discuss product compatibility questions.', '{"requested_by":"chatbot"}')
on conflict (id) do nothing;

insert into public.support_tickets (id, user_id, subject, description, status, priority, category, metadata_json) values
  ('60000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000001', 'Package tracking has not updated', 'Customer reports that the tracking link has shown label created for three days.', 'open', 'normal', 'shipping', '{"order_number":"MS-1042"}'),
  ('60000000-0000-0000-0000-000000000002', '10000000-0000-0000-0000-000000000002', 'Nebulizer kit compatibility', 'Customer wants to confirm whether the adult replacement kit fits their compressor model.', 'pending_customer', 'high', 'product_question', '{"product_sku":"MS-NEB-KIT-ADULT"}')
on conflict (id) do nothing;

insert into public.conversations (id, user_id, support_ticket_id, channel, status, summary, metadata_json) values
  ('70000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000001', '60000000-0000-0000-0000-000000000001', 'web', 'active', 'Customer asked about stalled package tracking.', '{"entrypoint":"order_status_widget"}'),
  ('70000000-0000-0000-0000-000000000002', '10000000-0000-0000-0000-000000000002', '60000000-0000-0000-0000-000000000002', 'email', 'waiting', 'Compatibility question escalated for staff review.', '{"entrypoint":"support_email"}')
on conflict (id) do nothing;

insert into public.messages (conversation_id, sender_type, content, metadata_json) values
  ('70000000-0000-0000-0000-000000000001', 'customer', 'My package tracking has not moved since Monday. Can you check it?', '{"intent":"order_status"}'),
  ('70000000-0000-0000-0000-000000000001', 'assistant', 'I can help check that. I found your order number and created a support ticket for shipping review.', '{"grounded":true}'),
  ('70000000-0000-0000-0000-000000000002', 'customer', 'Will this nebulizer replacement kit fit my older compressor?', '{"intent":"product_compatibility"}'),
  ('70000000-0000-0000-0000-000000000002', 'assistant', 'I need the compressor model number to confirm compatibility. I have sent a follow-up request.', '{"needs_customer_info":true}');

insert into public.agent_runs (id, conversation_id, support_ticket_id, run_type, status, model_name, input_payload, output_payload, started_at, completed_at) values
  ('80000000-0000-0000-0000-000000000001', '70000000-0000-0000-0000-000000000001', '60000000-0000-0000-0000-000000000001', 'ticket_triage', 'succeeded', 'gpt-4.1-mini', '{"message":"tracking has not moved"}', '{"category":"shipping","priority":"normal"}', now() - interval '1 hour', now() - interval '59 minutes'),
  ('80000000-0000-0000-0000-000000000002', '70000000-0000-0000-0000-000000000002', '60000000-0000-0000-0000-000000000002', 'rag_answer', 'succeeded', 'gpt-4.1-mini', '{"question":"nebulizer compatibility"}', '{"answer":"request model number","confidence":0.64}', now() - interval '30 minutes', now() - interval '29 minutes')
on conflict (id) do nothing;
